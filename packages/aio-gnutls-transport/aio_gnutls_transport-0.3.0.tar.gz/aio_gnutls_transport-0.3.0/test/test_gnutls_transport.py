#!/usr/bin/python3

import asyncio
import collections
from   contextlib import contextmanager, suppress
try:
    from contextlib import asynccontextmanager, nullcontext
except ImportError:
    # py3.6
    from async_generator import asynccontextmanager
    @contextmanager
    def nullcontext():
        yield
import logging
import os
import re
import socket
import subprocess
import ssl as native_ssl
import sys
import tempfile
import traceback
import types
from   typing import Optional, Union
from   unittest import TestCase, mock

if hasattr(asyncio.base_events, "_FATAL_ERROR_IGNORE"):
    # patch for asyncio<3.7.4 (report all server-side ssl errors in the logs)
    # https://bugs.python.org/issue37035
    asyncio.base_events._FATAL_ERROR_IGNORE = OSError,

from   aio_gnutls_transport import GnutlsEventLoopPolicy, GnutlsEventLoop, GnutlsError, lib
import aio_gnutls_transport.ssl as gnutls_ssl
from   .test_common import PY36, EnsureNoTestOverride, patch_lib


TestCase.__str__ = TestCase.id

LOOP_TIMEOUT=2

log = logging.getLogger("test")
#logging.basicConfig(level="DEBUG")

Connection = collections.namedtuple("Connection", ("server", "crd", "cwr", "srd", "swr"))

# possible initialisers for building a SSL context
# - None            -> no context (plain text socket)
# - ssl.SSLContext  -> a SSLContext object (already built)
# - dict            -> arguments for building the context with make_context()
SSLContextInit = Union[None, native_ssl.SSLContext, dict]

CERT_DIR = "test/certs"
def crt(name: str) -> str:
    return f"{CERT_DIR}/{name}.crt"
def key(name: str) -> str:
    return f"{CERT_DIR}/{name}.key"

def gen_cert(name: str, *, bits: int = 2048, ca: bool = False,
        dns_name: Optional[str] = None, issuer: Optional[str] = None):
    
    log.info(f"generating certificate {crt(name)}")

    def run(cmd):
        with subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            out, _ = proc.communicate()

        if proc.returncode:
            sys.stderr.write(out.decode(errors="replace"))
            raise subprocess.CalledProcessError(proc.returncode, cmd)


    with tempfile.NamedTemporaryFile(mode="w") as template:
        template.write(f"""
        cn = {name}
        expiration_days = 365
        """)
        if ca:
            template.write("ca\n")
        if dns_name:
            template.write(f"dns_name = {dns_name}\n")
        template.flush()

        run(["certtool", "--generate-privkey",
            "--bits", str(bits), "--outfile", key(name)])

        cmd = ["certtool"]
        if issuer is None:
            cmd += ["--generate-self-signed"]
        else:
            cmd += ["--generate-certificate",
                    "--load-ca-privkey", key(issuer),
                    "--load-ca-certificate", crt(issuer)]
        cmd += ["--template", template.name, "--load-privkey", key(name),
                "--outfile", crt(name)]
        run(cmd)

def make_context(purpose: int, *,
        cert: Optional[str] = None,
        ca: Optional[str] = None,
        verify_mode: Optional[int] = None,
        can_write_eof: Optional[bool] = None, 
        ssl: Optional[types.ModuleType] = None):
    if ssl is None:
        ssl = globals()["ssl"]
    ctx = ssl.create_default_context(purpose,
            cafile = (None if ca is None else crt(ca)))
    if verify_mode is not None:
        ctx.verify_mode = verify_mode
    if cert is not None:
        ctx.load_cert_chain(crt(cert), key(cert))
    if can_write_eof is not None:
        ctx.can_write_eof = can_write_eof
    return ctx

def gnutls_event_loop(func):
    def wrapper(self):
        self._loop.close()
        self._loop = GnutlsEventLoop()
        asyncio.set_event_loop(self._loop)
        return func(self)
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return wrapper


def aiotest(func):
    def wrapper(self):
        self._loop.run_until_complete(
                asyncio.wait_for(func(self), LOOP_TIMEOUT))
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return wrapper

def aiotest_with_default_connection(func):
    async def wrapper(self):
        async with self.default_tls_connection() as conn:
            await func(self, conn)
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    return aiotest(wrapper)

    

class _TransportTestCaseMixin(EnsureNoTestOverride):

    @classmethod
    def setUpClass(cls):
        asyncio.set_event_loop_policy(cls._policy_factory())
        globals()["ssl"] = cls._ssl_module

        if not hasattr(_TransportTestCaseMixin, "certificates"):
            if not os.path.isdir(CERT_DIR):
                os.mkdir(CERT_DIR)

            gen_cert("localhost", dns_name="localhost")
            gen_cert("anotherhost", dns_name="anotherhost")
            gen_cert("users-ca", ca=True)
            gen_cert("user1", issuer="users-ca")

            certs = {}
            for name in "localhost", "users-ca", "user1":
                with open(crt(name)) as fp:
                    certs[ssl.PEM_cert_to_DER_cert(fp.read())] = name
            _TransportTestCaseMixin.certificates = certs

    @classmethod
    def tearDownClass(cls):
        del globals()["ssl"]


    def setUp(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def tearDown(self):
        self._loop.set_debug(True)
        self._loop.close()

    async def assertNotEof(self, reader, count=8):
        with self.assertRaises(asyncio.TimeoutError):
            fut = asyncio.ensure_future(reader.read(count))
            data = await asyncio.wait_for(fut, .05)
            assert 0, f"read() must not return (got {data})"
        if PY36:
            # cleanup needed (otherwise next .read() would fail)
            with suppress(asyncio.CancelledError):
                await fut

    def default_tls_connection(self):
        return self.tls_connection(
                cli={"ca": "localhost"}, srv={"cert": "localhost"})

    @asynccontextmanager
    async def tls_connection(self, cli: SSLContextInit, srv: SSLContextInit, *,
            unix: bool = False) -> None:
        cli_ctx = cli if not isinstance(cli, dict) else make_context(
                ssl.Purpose.SERVER_AUTH, **cli)
        srv_ctx = srv if not isinstance(srv, dict) else make_context(
                ssl.Purpose.CLIENT_AUTH, **srv)

        incoming = asyncio.Future()
        def handle_client(reader, writer):
            incoming.set_result((reader, writer))

        @asynccontextmanager
        async def run_client():
            crd = cwr = srd = swr = None
            try:
                # run the client
                crd, cwr = await opener
                try:
                    srd, swr = await asyncio.wait_for(incoming, 0.5)
                except asyncio.TimeoutError:
                    pass
                yield Connection(server, crd, cwr, srd, swr)
            finally:
                log.debug("tls_connection cleanup")
                for writer in cwr, swr:
                    if writer is not None:
                        if sys.exc_info()[0] is None:
                            writer.close()
                        else:
                            writer.transport.abort()
                for writer in cwr, swr:
                    if writer is not None and not PY36:
                        with suppress(OSError):
                            await writer.wait_closed()
                server.close()

        if unix:
            with tempfile.TemporaryDirectory() as tmp:
                path = f"{tmp}/socket"

                # create the server
                server = await asyncio.start_unix_server(
                        handle_client, path, ssl=srv_ctx)

                # run the client
                opener = asyncio.open_unix_connection(path, ssl=cli_ctx, 
                        server_hostname=(None if cli_ctx is None else "localhost"))
                async with run_client() as c:
                    yield c
        else:
            # create the server
            server = await asyncio.start_server(handle_client, "localhost",
                    family=socket.AF_INET, ssl=srv_ctx)
            port = server.sockets[0].getsockname()[1]

            # run the client
            opener = asyncio.open_connection("localhost", port, ssl=cli_ctx)
            async with run_client() as c:
                yield c


    def check_tls_connection(self, cli: SSLContextInit, srv: SSLContextInit, *,
            unix: bool = False):
        @aiotest
        async def test_func(self):
            async with self.tls_connection(cli, srv, unix=unix) as conn:
                conn.cwr.write(b"foo")
                self.assertEqual(await conn.srd.read(32), b"foo")
                conn.swr.write(b"bar")
                self.assertEqual(await conn.crd.read(32), b"bar")

        test_func(self)


    def assertPeerCertIs(self, writer, name):
        sobj = writer.transport.get_extra_info("ssl_object")
        peercert = sobj.getpeercert(True)
        if name is None:
            self.assertIs(peercert, None)
        else:
            peercert = self.certificates.get(peercert, peercert)
            self.assertEqual(peercert, name)


    @contextmanager
    def assertClientError(self, error_id):
        regex = self._ERRORS[error_id]
        try:
            yield
            exc = None
        except Exception as e:
            txt = traceback.format_exception_only(e.__class__, e)[-1].strip()
            if re.search(regex, txt, re.S):
                return
            raise AssertionError(f"client error {regex!r} not matched in {txt!r}") from e
        else:
            raise AssertionError(f"client error {regex!r} not raised")


    @contextmanager
    def assertServerError(self, error_id, *, level=None):
        regex = self._ERRORS[error_id]
        if level is not None:
            int_level = level if isinstance(level, int
                    ) else logging.getLevelName(level)
            assert isinstance(int_level, int), f"invalid logging level {level!r}"

        try:
            with self.assertLogs("asyncio", level) as watcher:
                yield
        finally:
            logger = logging.getLogger("asyncio")
            found = False
            for record, output in zip(watcher.records, watcher.output):
                if not found:
                    if level is None or record.levelno == int_level:
                        if re.search(regex, output, re.S):
                            found = True
                            continue
                logger.handle(record)

            if not found:
                records = "".join(f"\n - {r}" for r in watcher.output)
                raise AssertionError(f"""server error {regex!r}{
                        "" if level is None else f" with level {level}"
                    } not matched in 'asyncio' logs{f":{records}" if records else ""
                    }""")



    def test_server_auth(self):
        test = lambda unix: self.check_tls_connection(
                cli={"ca":   "localhost"},
                srv={"cert": "localhost"}, unix=unix)

        test(False) # TCP
        test(True)  # unix


    def test_native_ssl_context(self):
        def test(unix):
            # native client
            cli = native_ssl.create_default_context( cafile=crt("localhost"))
            self.check_tls_connection( cli=cli, srv={"cert": "localhost"},
                    unix=unix)

            # native server
            srv = native_ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            srv.load_cert_chain(crt("localhost"), key("localhost"))
            self.check_tls_connection(cli={"ca": "localhost"}, srv=srv,
                    unix=unix)

        test(False) # TCP
        test(True)  # unix


    def test_plain_text_connection(self):
        def test(unix):
            # native client
            self.check_tls_connection(cli=None, srv=None, unix=unix)

            # native server
            self.check_tls_connection(cli=None, srv=None, unix=unix)

        test(False) # TCP
        test(True)  # unix


    def test_server_auth_fail_unknown_issuer(self):

        def test():
            with self.assertClientError("UNKNOWN_ISSUER"):
                self.check_tls_connection(cli={}, srv={"cert": "localhost"})
        test()

        self._loop.set_debug(True)
        with self.assertServerError("CONNECTION_RESET", level="ERROR"):
            test()

    def test_server_auth_fail_hostname_mismatch(self):

        def test(unix):
            def run():
                with self.assertClientError("HOSTNAME_MISMATCH"):
                    self.check_tls_connection(
                            cli={"ca": "anotherhost"},
                            srv={"cert": "anotherhost"}, unix=unix)

            self._loop.set_debug(False)
            run()

            self._loop.set_debug(True)
            with self.assertServerError("CONNECTION_RESET", level="ERROR"):
                run()

        if PY36 and ssl is native_ssl:
            # py3.6's native ssl returns different errors
            # -> just skip
            return

        test(False) # TCP
        test(True)  # unix

    @aiotest
    async def test_client_auth(self):
        for verify_mode, user_cert, expected in (
                (None,              None,       None),
                (None,              "user1",    None),
                (ssl.CERT_NONE,     None,       None),
                (ssl.CERT_NONE,     "user1",    None),
                (ssl.CERT_OPTIONAL, None,       None),
                (ssl.CERT_OPTIONAL, "user1",    "user1"),
                (ssl.CERT_REQUIRED, "user1",    "user1"),
                ):
            with self.subTest(verify_mode=verify_mode):
                async with self.tls_connection(
                        cli=dict(ca="localhost", cert=user_cert),
                        srv=dict(cert="localhost", ca="users-ca",
                            verify_mode=verify_mode),
                        ) as conn:
                    self.assertPeerCertIs(conn.cwr, "localhost")
                    self.assertPeerCertIs(conn.swr, expected)

    
        async def test_cert_required():
            with self.assertClientError("CONNECTION_RESET"):
                async with self.tls_connection(
                        cli=dict(ca="localhost"),
                        srv=dict(cert="localhost", ca="users-ca",
                            verify_mode=ssl.CERT_REQUIRED)) as conn:
                    self.assertIs(conn.swr, None)
                    await conn.cwr.drain()

        await test_cert_required()

        self._loop.set_debug(True)
        with self.assertServerError("NO_PEER_CERT", level="ERROR"):
            await test_cert_required()


    @gnutls_event_loop
    @aiotest
    async def test_no_write_eof(self):

        kw = {} if ssl is native_ssl else {"can_write_eof": False}
        async with self.tls_connection(
                cli={"ca": "localhost", "ssl": gnutls_ssl},
                srv={"cert": "localhost", **kw}) as conn:
            self.assertTrue(conn.cwr.can_write_eof())
            self.assertFalse(conn.swr.can_write_eof())

            # client eof
            await self.assertNotEof(conn.srd)
            conn.cwr.write_eof()
            self.assertEqual(await conn.srd.read(8), b"")

            # server eof too (half-close not supported)
            self.assertEqual(await conn.crd.read(8), b"")


    @aiotest_with_default_connection
    async def test_write_args_check(self, conn):
        
        conn.cwr.write(b"[bytes]")
        conn.cwr.write(bytearray(b"[bytearray]"))
        conn.cwr.write(memoryview(b"[memoryview]"))

        self.assertRaisesRegex(
                TypeError, "data: expecting a bytes-like instance, got ('str'|str)",
                conn.cwr.write, "[str]")

        conn.cwr.write(b"")

        conn.cwr.write(b"\n")
        self.assertEqual(await conn.srd.readline(),
                b"[bytes][bytearray][memoryview]\n")



class GnutlsTransportTestCase (_TransportTestCaseMixin, TestCase):
    _policy_factory = GnutlsEventLoopPolicy
    _ssl_module = gnutls_ssl


    def _tls_error(e, t):
        return f"aio_gnutls_transport.GnutlsError:.*({t}).*\\(({e})\\)"
    def _cert_error(t):
        return ("aio_gnutls_transport.GnutlsError:"
            +f".*The certificate is NOT trusted.*({t})"
            +".*\\(GNUTLS_E_CERTIFICATE_ERROR\\)")

    _ERRORS = {
            "CONNECTION_RESET": "ConnectionResetError",

            "NO_PEER_CERT":     _tls_error(
                "GNUTLS_E_CERTIFICATE_REQUIRED|GNUTLS_E_NO_CERTIFICATE_FOUND",
                "Certificate is required|No certificate was found"),

            "UNKNOWN_ISSUER":   _cert_error(
                "The certificate issuer is unknown"),

            "HOSTNAME_MISMATCH":_cert_error(
                "The name in the certificate does not match the expected")
            }

    @asynccontextmanager
    async def fill_write_buffer(self, writer, first=b"foo\n", second=b"bar\n"):
        buff = writer.transport._buffer
        self.assertFalse(buff)
        with mock.patch.object(self._loop, "_add_writer") as m_addw, \
                patch_lib("gnutls_record_send",
                        return_value = lib._GNUTLS_E_AGAIN) as m_send:

            # first write
            writer.write(first)
            m_send.assert_called()
            m_addw.assert_called_once()
            addw_args = m_addw.call_args
            self.assertEqual(addw_args[0][0], writer.transport._sock_fd)
            self.assertEqual(buff, first)

            m_send.reset_mock()
            m_addw.reset_mock()

            # second write
            writer.write(second)
            m_send.assert_not_called()
            m_addw.assert_not_called()
            self.assertEqual(buff, first+second)

            # loop callback but send() returns E_AGAIN
            writer.transport._write_ready()
            m_send.assert_called_once()
            m_addw.assert_not_called()

            m_send.reset_mock()

        yield lambda: self._loop._add_writer(*addw_args[0], **addw_args[1])

    @aiotest_with_default_connection
    async def test_write_eof(self, conn):
            # client write
            await self.assertNotEof(conn.srd)
            conn.cwr.write(b"hello")
            self.assertEqual(await conn.srd.read(8), b"hello")

            # client eof
            await self.assertNotEof(conn.srd)
            conn.cwr.write_eof()
            self.assertEqual(await conn.srd.read(8), b"")

            self.assertRaisesRegex(
                    RuntimeError, "Cannot call write\\(\\) after write_eof\\(\\)",
                    conn.cwr.write, b"hello bad")

            # server write
            await self.assertNotEof(conn.crd)
            conn.swr.write(b"world")
            self.assertEqual(await conn.crd.read(8), b"world")

            # server eof
            await self.assertNotEof(conn.crd)
            conn.swr.write_eof()
            self.assertEqual(await conn.crd.read(8), b"")


    @aiotest_with_default_connection
    async def test_read_buffer_full(self, conn):
        with mock.patch("aio_gnutls_transport._read_buffer", bytearray(4)):
            DATA = b"foo bar FOO BAR\n"
            conn.cwr.write(DATA)
            self.assertEqual(await conn.srd.readline(), DATA)
    
    @aiotest_with_default_connection
    async def test_write_bufferred(self, conn):
        with mock.patch("aio_gnutls_transport._read_buffer", bytearray(4)):

            # direct write
            with mock.patch.object(self._loop, "_add_writer") as m:
                conn.cwr.write(b"foo\n")
                self.assertEqual(await conn.srd.readline(), b"foo\n")
            m.assert_not_called()


            # bufferred write
            async with self.fill_write_buffer(conn.cwr) as release:
                await self.assertNotEof(conn.srd, 1)
                release()

                self.assertEqual(await conn.srd.read(8), b"foo\nbar\n")
                self.assertFalse(conn.cwr.transport._buffer)

            # bufferred write w/ close()
            async with self.fill_write_buffer(conn.cwr) as release:
                conn.cwr.close()
                await self.assertNotEof(conn.srd, 1)
                release()

                self.assertEqual(await conn.srd.read(), b"foo\nbar\n")
                self.assertFalse(conn.cwr.transport._buffer)
                conn.swr.close()
                if not PY36:
                    self.assertFalse(await conn.cwr.wait_closed())

    
    @aiotest_with_default_connection
    async def test_write_bufferred_eof(self, conn):
        with mock.patch("aio_gnutls_transport._read_buffer", bytearray(4)):

            async with self.fill_write_buffer(conn.cwr) as release:
                conn.cwr.write_eof()
                await self.assertNotEof(conn.srd, 1)
                release()

                self.assertEqual(await conn.srd.read(), b"foo\nbar\n")
                self.assertFalse(conn.cwr.transport._buffer)

                conn.swr.write(b"not finished\n")
                self.assertEqual(await conn.crd.readline(), b"not finished\n")


class OpensslTransportTestCase (_TransportTestCaseMixin, TestCase):
    _policy_factory = asyncio.DefaultEventLoopPolicy
    _ssl_module = native_ssl

    _ERRORS = {
            "CONNECTION_RESET": "ConnectionResetError",

            "NO_PEER_CERT":     "ssl.SSLError:"
                                +".*PEER_DID_NOT_RETURN_A_CERTIFICATE",

            "UNKNOWN_ISSUER":   "ssl.SSLCertVerificationError:"
                                +".*self signed certificate"
                                +"|ssl.SSLError:.*certificate verify failed", # py3.6

            "HOSTNAME_MISMATCH":"ssl.SSLCertVerificationError:"
                                +".*Hostname mismatch, certificate is not valid for"
                                +"|ssl.CertificateError.*hostname '.*' doesn't match '.*'", # py3.6
            }



