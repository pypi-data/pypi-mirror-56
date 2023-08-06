#!/usr/bin/python3

import asyncio
import logging
import socket
import sys
from   typing import Callable, ClassVar, Dict, Optional, Tuple, Union
import weakref

from aio_gnutls_transport._gnutls import ffi, lib
from .stdlib import _SelectorTransport, LOG_THRESHOLD_FOR_CONNLOST_WRITES


DEFAULT_PRIORITY = "SECURE:-RSA:%PROFILE_MEDIUM:%SERVER_PRECEDENCE"

log = logging.getLogger("aio_gnutls_transport")

_read_buffer = bytearray(0x10000)
_Loop = asyncio.AbstractEventLoop
_ProtocolFactory = Callable[[], asyncio.Protocol]

# mitigation for https://bugs.python.org/issue33263
_HAVE_BPO_33263 = sys.version_info[:3] < (3,6,6)

def _as_void_ptr(cdata):
    return ffi.cast("void **", ffi.addressof(cdata))[0]

class _GlobalHandle:
    def __init__(self) -> None:
        log.debug("global init")
        lib.gnutls_global_init()
        return None

    def __del__(self) -> None:
        log.debug("global deinit")
        lib.gnutls_global_deinit()
        return None

_global_handle = _GlobalHandle()

# NOTE: when `status` is provided, the function assumes that the credentials
#       are using X509 certificates
def _make_error(err: int, status: Optional[int] = None) -> OSError:

    if status is not None and err == lib._GNUTLS_E_CERTIFICATE_ERROR:
        # for certificate validation error, we generate the error msg from the
        # `status` (if available) which is more useful
        dt = ffi.new("gnutls_datum_t*")
        if lib.gnutls_certificate_verification_status_print(
                status, lib.GNUTLS_CRT_X509, dt, 0) == 0:
            try:
                if dt.size:
                    return GnutlsError("GNUTLS_E_CERTIFICATE_ERROR",
                            ffi.string(dt.data, dt.size).strip().decode())
            finally:
                lib.gnutls_free(dt.data)
    elif err in (lib._GNUTLS_E_PULL_ERROR, lib._GNUTLS_E_PUSH_ERROR):
        # push/pull errors are not very helpful (because gnutls ignores errno)
        #
        # we raise ConnectionResetError instead (which is actually what the
        # native ssl transport does)
        return ConnectionResetError("Connection lost")

    nameptr = lib.gnutls_strerror_name(err)
    if nameptr == ffi.NULL:
        name = err
        msg  = "Gnutls error %d" % err
    else:
        name = ffi.string(nameptr).decode()
        msgptr = lib.gnutls_strerror(err)
        msg = name if msgptr is None else ffi.string(msgptr).decode()

    return GnutlsError(name, msg)

#TODO handle received alerts for gnutls_recv_record() and gnutls_handshake()
def _check_error(err: int) -> int:
    if err < 0:
        raise _make_error(err)
    return err

def _session_id(session: "lib.session_t") -> bytes:
    """Return a hashable id of a gnutls session"""
    return bytes(ffi.buffer(ffi.addressof(session)))

def _register_fd_events(loop: _Loop, fd: int, session: "lib.session_t",
        callback: Callable[[], None]) -> None:
    """Register socket callbacks for gnutls IOs that are bidirectionnal"""
    if lib.gnutls_record_get_direction(session):
        # interrupted while writing
        log.debug("interrupted while writing on fd %r", fd)
        loop._add_writer(fd, callback)
        loop._remove_reader(fd)
    else:
        # interrupted while reading
        log.debug("interrupted while reading on fd %r", fd)
        loop._add_reader(fd, callback)
        loop._remove_writer(fd)

def _unregister_fd_events(loop: _Loop, fd: int) -> None:
    """Unregister all callbacks for a socket"""
    log.debug("unregister callbacks on fd %r", fd)
    loop._remove_reader(fd)
    loop._remove_writer(fd)


class GnutlsError(OSError):
    args: Tuple[Union[str, int], str]

    # NOTE: may return an int
    @property
    def name(self) -> Union[str, int]:
        return self.args[0]

    def __str__(self) -> str:
        return "{1} ({0})".format(*self.args)


class GnutlsEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self) -> _Loop:
        return GnutlsEventLoop()

class GnutlsEventLoop(asyncio.SelectorEventLoop):

    async def create_connection(self, protocol_factory: _ProtocolFactory,
            host=None, port=None, *, ssl=None, server_hostname=None, **kw):
        if isinstance(ssl, GnutlsContext):
            waiter = self.create_future()
            transport, protocol = await super().create_connection(
                    lambda: GnutlsHandshakeProtocol(
                        self, protocol_factory, ssl, False,
                        (host if server_hostname is None else server_hostname),
                        waiter),
                    host, port, **kw)
            return await waiter
        else:
            return await super().create_connection(protocol_factory, host, port,
                    ssl=ssl, server_hostname=server_hostname, **kw)

    async def create_server(self, protocol_factory: _ProtocolFactory, *k,
            ssl=None, **kw):
        if isinstance(ssl, GnutlsContext):
            return await super().create_server(
                    lambda: GnutlsHandshakeProtocol(
                        self, protocol_factory, ssl, True, None, None),
                    *k, **kw)
        else:
            return await super().create_server(
                    protocol_factory, *k, ssl=ssl, **kw)

    async def create_unix_connection(self, protocol_factory: _ProtocolFactory,
            path=None, *, ssl=None, server_hostname=None, **kw):
        if isinstance(ssl, GnutlsContext):
            if server_hostname is None:
                raise ValueError(
                        "you have to pass server_hostname when using ssl")
            waiter = self.create_future()
            transport, protocol = await super().create_unix_connection(
                    lambda: GnutlsHandshakeProtocol(self, protocol_factory,
                        ssl, False, server_hostname, waiter),
                    path, **kw)
            return await waiter
        else:
            return await super().create_unix_connection(protocol_factory,
                    path, ssl=ssl, server_hostname=server_hostname, **kw)

    async def create_unix_server(self, protocol_factory: _ProtocolFactory,
            path=None, *, ssl=None, **kw):
        if isinstance(ssl, GnutlsContext):
            return await super().create_unix_server(
                    lambda: GnutlsHandshakeProtocol(
                        self, protocol_factory, ssl, True, None, None),
                    path, **kw)
        else:
            return await super().create_unix_server(
                    protocol_factory, path, ssl=ssl, **kw)

def _maybe_release_session(session: "Optional[lib.session_t]") -> None:
    if session is not None:
        log.debug("session deinit")
        lib.gnutls_deinit(session)

def _maybe_release_credentials(cred: "Optional[lib.cred_t]") -> None:
    if cred is not None:
        log.debug("cred free")
        lib.gnutls_certificate_free_credentials(cred)

class GnutlsContext:
    # keep a reference on the global_handle to prevent gnutls_global_deinit()
    # if we still have active objects
    __global_handle: ClassVar[_GlobalHandle] = _global_handle

    _init_flags: int
    _priority: Optional[str]
    can_write_eof: bool

    def __init__(self) -> None:
        self._init_flags = 0
        self._priority = None
        self.can_write_eof = True

        ptr = ffi.new("gnutls_certificate_credentials_t*")
        _check_error(lib.gnutls_certificate_allocate_credentials(ptr))
        self._cred = ptr[0]

        # We require strict ordering of certificate chains because we rely on
        # gnutls_certificate_get_peers() to get the peer certificate
        # (gnutls transparently handles unsorted cert chains, but does not
        #  provide any api endpoint to get the sorted chain)
        lib.gnutls_certificate_set_verify_flags(self._cred,
                lib.GNUTLS_VERIFY_DO_NOT_ALLOW_UNSORTED_CHAIN)

    def __del__(self) -> None:
        cred = getattr(self, "_cred")
        if cred is not None:
            lib.gnutls_certificate_free_credentials(cred)

        if self._priority is not None:
            lib.gnutls_priority_deinit(self._priority)

    # to be used with care because some flags may badly interfer with
    # GnutlsTransport defaults
    def gnutls_set_init_flags(self, flags: int) -> None:
        self._init_flags = flags

    def gnutls_set_priority(self, priority: Optional[str]) -> None:
        if self._priority is not None:
            lib.gnutls_priority_deinit(self._priority)
            self._priority = None

        if priority is None:
            return
        
        ptr = ffi.new("gnutls_priority_t*")
        buf = ffi.from_buffer(priority.encode())
        err_pos = ffi.new("char**")
        if lib.gnutls_priority_init(ptr, buf, err_pos) == 0:
            self._priority = ptr[0]
        else:
            msg = "invalid priority string"
            if err_pos[0] != ffi.NULL:
                msg += " at %r" % ffi.string(err_pos[0]).decode(errors="replace")[:32]
            raise GnutlsError("GNUTLS_E_INVALID_REQUEST", msg)

    def _gnutls_cert_required(self) -> bool:
        """Return True if we require certificate authentication from the peer"""
        raise NotImplementedError

    def _gnutls_verify_cert(self) -> bool:
        """Return True if we request certificate authentication from the peer"""
        raise NotImplementedError

    def _gnutls_check_hostname(self) -> bool:
        """Return True if we need to check the hostname against the certificate"""
        raise NotImplementedError

    def load_cert_chain(self, certfile: str , keyfile: Optional[str] = None,
            password: Optional[str] = None) -> None:
        _check_error(lib.gnutls_certificate_set_x509_key_file2(self._cred,
            certfile.encode(),
            (keyfile or "").encode(),
            lib.GNUTLS_X509_FMT_PEM,
            (password or "").encode(), 0))

    def load_verify_locations(self, cafile: Optional[str] = None,
            capath: Optional[str] = None, cadata: Optional[str] = None) -> None:
        if capath is not None or cadata is not None:
            raise NotImplementedError("'capath' and 'cadata' not supported")
        if cafile is not None:
            _check_error(lib.gnutls_certificate_set_x509_trust_file(self._cred,
                    cafile.encode(), lib.GNUTLS_X509_FMT_PEM))
        else:
            raise TypeError("cafile, capath and cadata cannot be all omitted")

    def load_default_certs(self) -> None:
        _check_error(lib.gnutls_certificate_set_x509_system_trust(self._cred))

class GnutlsObject:
    context: GnutlsContext

    def __init__(self, context: GnutlsContext, peer_cert: Optional[bytes]) -> None:
        self.context = context
        self._peer_cert = peer_cert     # DER format

    def getpeercert(self, binary_form: bool = False) -> Optional[bytes]:
        if binary_form:
            return self._peer_cert
        else:
            raise NotImplementedError


class GnutlsHandshakeProtocol(asyncio.Protocol):
    # keep a reference on the global_handle to prevent gnutls_global_deinit()
    # if we still have active objects
    __global_handle: ClassVar[_GlobalHandle] = _global_handle

    # global dict of all GnutlsHandshakeProtocol objects
    #
    # key: gnutls session id
    # value: GnutlsHandshakeProtocol
    __objects: """ClassVar[Dict[bytes, GnutlsHandshakeProtocol]
            ]""" = weakref.WeakValueDictionary()

    # global dict of credentials used by each session
    #
    # The only purpose of this dict is to prevent credentials objects to be
    # destroyed before the session objects using them.
    #
    # We need it because the gnutls_session_t keeps a pointer to the relevant
    # gnutls_certificate_credentials_t, it is our responsibility to ensure that
    # this pointer always remains valid.
    #
    # key: gnutls_session_t
    # value: GnutlsContext
    __credentials_dict: """ClassVar[Dict[lib.session_t, GnutlsContext]
            ]""" = weakref.WeakKeyDictionary()

    _loop: _Loop
    _protocol_factory: _ProtocolFactory
    _waiter: Optional[asyncio.Future]
    _transport: Optional[asyncio.Transport]
    _sock: socket.socket
    _sock_fd: int
    _server_side: bool
    #_hostname: bytes or ffi.NULL
    _context: GnutlsContext
    _status: Optional[int]
    _peer_cert: Optional[bytes]
    _session: "lib.session_t"

    def __init__(self, loop: _Loop, protocol_factory: _ProtocolFactory,
            context: GnutlsContext, server_side: bool, hostname: Optional[str],
            waiter: Optional[asyncio.Future]) -> None:

        self._loop = loop
        self._protocol_factory = protocol_factory
        self._waiter = waiter
        self._transport = None
        self._server_side = server_side
        self._context = context
        if hostname is not None and context._gnutls_check_hostname():
            self._hostname = hostname.encode()
        else:
            self._hostname = ffi.NULL
        self._status = None

        # peer certificate in the DER format
        # 
        # set only if the peer certificate was successfully verified
        self._peer_cert = None

        self._session = self._create_session(server_side)
        self.__objects[_session_id(self._session)] = self

    def __del__(self) -> None:
        _maybe_release_session(getattr(self, "_session", None))

    @staticmethod
    @ffi.def_extern()
    def _aio_gnutls_verify_cert_callback(session: "lib.session_t") -> int:
        """Callback function called by gnutls for validating peer certificates"""
        try:
            log.debug("_aio_gnutls_verify_cert_callback")
            self = GnutlsHandshakeProtocol.__objects.get(_session_id(session))

            if self is None:
                # should never happen
                log.warning("verify_cert_callback called with unknown gnutls session id")
                return -1

            # reset the peer certificate to a safe value
            # (unset means: 'remote is not authenticated'
            self._peer_cert = None

            # verify the certificate
            status = ffi.new("unsigned int*")
            err = lib.gnutls_certificate_verify_peers3(session, self._hostname, status)
            if err:
                if (err==lib._GNUTLS_E_NO_CERTIFICATE_FOUND
                        and not self._context._gnutls_cert_required()):
                    # cert is optional and peer did not provide any
                    # -> handshake success
                    return 0
                else:
                    log.debug("%r: gnutls_certificate_verify_peers3 failed (error %d)",
                            self, err)
            elif status[0] != 0:
                self._status = status[0]
                log.debug("%r: certificate verify failed, status %d", self,
                        status[0])
            else:
                # success

                # get the peer certificate
                list_size = ffi.new("unsigned int*")
                datum = lib.gnutls_certificate_get_peers(self._session, list_size)
                if datum != ffi.NULL and list_size[0] > 0:
                    assert (lib.gnutls_certificate_get_verify_flags(self._context._cred)
                            & lib.GNUTLS_VERIFY_DO_NOT_ALLOW_UNSORTED_CHAIN)
                    self._peer_cert = bytes(datum.data[0:datum.size])
                    log.debug("%r: peer cert verified", self)

                    # handshake success
                    return 0
                else:
                    # should never happen
                    log.debug("%r: could not get peer certificate", self)

            # handshake failure
            return -1

        except:
            # NOTE: it is critical that we reliably return -1 in case any
            # exception is raised because cffi's default exception handler
            # returns 0 (which would accept the certificate)
            try:
                log.exception("unhandled exception in _aio_gnutls_verify_cert_callback")
            except:
                pass
            return -1

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        log.debug("%r: connection made %r", self, transport)

        # steal the socket from the TCP transport and kill the transport
        sock = transport.get_extra_info("socket")
        self._sock = sock.dup()
        self._sock_fd = self._sock.fileno()
        if _HAVE_BPO_33263:
            # this is an ugly mitigation (safe if not multithreaded)
            sock.close()
        transport.abort()

        lib.gnutls_transport_set_int(self._session, self._sock.fileno())

        # start the handshake
        self._handshake()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        log.debug("%r: connection lost", self)
        if not hasattr(self, "_session"):
            # handshake is successful
            if exc is None:
                # normal case (no exception)
                return
            else:
                log.exception("unexpected exception after successful handshake")
        else:
            # handshake in progress
            if exc is not None:
                # should never happen (errors reported by _handshake())
                log.exception("unexpected exception during handshake")


    def _create_session(self, server_side: bool) -> "lib.session_t":
        ctx = self._context

        ptr = ffi.new("gnutls_session_t*")
        role = lib.GNUTLS_SERVER if server_side else lib.GNUTLS_CLIENT
        _check_error(lib.gnutls_init(ptr,
            role | lib.GNUTLS_NONBLOCK | ctx._init_flags));
        session = ptr[0]

        if ctx._priority is None:
            _check_error(lib.gnutls_set_default_priority(session))
        else:
            _check_error(lib.gnutls_priority_set(session, ctx._priority))

        # NOTE: we store the context in self.__credentials_dict to ensure that
        #       the credentials will never be released before the session
        #       (because the session keeps a pointer to the credentials)
        self.__credentials_dict[session] = ctx 
        _check_error(lib.gnutls_credentials_set(session,
            lib.GNUTLS_CRD_CERTIFICATE, _as_void_ptr(ctx._cred)))


        # set up the callback for verifying the peer certificate
        if ctx._gnutls_verify_cert():
            lib.gnutls_session_set_verify_function(session, lib._aio_gnutls_verify_cert_callback)

            if server_side:
                # send a certificate request to the client
                lib.gnutls_certificate_server_set_request(session, (
                    lib.GNUTLS_CERT_REQUIRE if ctx._gnutls_cert_required()
                    else lib.GNUTLS_CERT_REQUEST))
        else:
            assert not ctx._gnutls_cert_required()

        if not server_side and self._hostname != ffi.NULL:
            # send the SNI extension
            lib.gnutls_server_name_set(session, lib.GNUTLS_NAME_DNS,
                    self._hostname, len(self._hostname))

        return session

    def _handshake(self) -> None:
        err = lib.gnutls_handshake(self._session)
        if err >= 0:
            # handshake completed
            log.debug("%r: handshake -> success", self)
            assert not (self._peer_cert is None and self._context._gnutls_cert_required())

            _unregister_fd_events(self._loop, self._sock_fd)

            protocol = self._protocol_factory()
            session = self._session
            del self._session
            ssl_object = GnutlsObject(self._context, self._peer_cert)
            transport = GnutlsTransport(self._loop, self._sock, session,
                    ssl_object, protocol, self._waiter,
                    self._context.can_write_eof)
        elif err == lib._GNUTLS_E_AGAIN or err == lib._GNUTLS_E_INTERRUPTED:
            log.debug("%r: handshake -> again", self)
            _register_fd_events(self._loop, self._sock_fd, self._session,
                    self._handshake)
        else:
            # TODO: handle non-fatal alerts (gnutls_handshake() may return
            #       GNUTLS_E_WARNING_ALERT_RECEIVED)
            exc = _make_error(err, self._status)
            log.debug("%r: handshake -> failed [%r]", self, exc)
            if self._waiter is None:
                if self._loop.get_debug():
                    self._loop.call_exception_handler(dict(
                        message="handshake failed on Gnutls transport",
                        exception=exc,
                        protocol=self))
            else:
                self._waiter.set_exception(exc)
            _unregister_fd_events(self._loop, self._sock_fd)
            self._sock.close()
            del self._sock
            del self._sock_fd


class GnutlsTransport(_SelectorTransport):
    # keep a reference on the global_handle to prevent gnutls_global_deinit()
    # if we still have active objects
    __global_handle: ClassVar[_GlobalHandle] = _global_handle

    ## BaseTransport ##

    _session: "lib.session_t"
    _protocol: asyncio.Protocol
    _can_write_eof: bool
    _eof_written: bool
    _shutdown_request: Optional[int]
    _paused: bool

    def __init__(self, loop: _Loop, sock: socket.socket, session:
            "lib.session_t", ssl_object: GnutlsObject, protocol:
            asyncio.Protocol, waiter: Optional[asyncio.Future], can_write_eof: bool):
        # store the session immediately (to avoid resources leak if
        # super().__init__ raise an exception)
        self._session = session

        #TODO: use Server._attach()/detach()
        #TODO: add missing extra infos
        #   cipher:         ('ECDHE-RSA-AES256-GCM-SHA384', 'TLSv1.2', 256)
        #   compression:    None
        #   peercert:       {'subject': ((('commonName', 'localhost'),),), 'issuer': ((('commonName', 'localhost'),),), 'version': 3, 'serialNumber': '5C6155061954F1F3BA911931', 'notBefore': 'Feb 11 10:57:10 2019 GMT', 'notAfter': 'Feb 11 10:57:10 2020 GMT', 'subjectAltName': (('DNS', 'localhost'),)}
        super().__init__(loop, sock, protocol, {
            "session": session,
            "ssl_object": ssl_object,
            "sslcontext": ssl_object.context,
            })
        
        self._can_write_eof = can_write_eof
        self._eof_written = False   # .write_eof() was called
        self._shutdown_request = None # pending shutdown (SHUT_WR or SHUT_RDWR)
        self._paused = False

        loop.call_soon(protocol.connection_made, self)
        # only start reading when connection_made() has been called
        loop.call_soon(self._add_reader, self._sock_fd, self._read_ready)

        if waiter is not None:
            # only wake up the waiter when connection_made() has been called
            @loop.call_soon
            def wake():
                if not waiter.cancelled():
                    waiter.set_result((self, protocol))


    def __del__(self) -> None:
        _maybe_release_session(getattr(self, "_session", None))

    def pause_reading(self) -> None:
        if self._closing or self._paused:
            return
        self._paused = True
        self._loop._remove_reader(self._sock_fd)
        if self._loop.get_debug():
            log.debug("%r: pauses reading", self)

    def resume_reading(self) -> None:
        if self._closing or not self._paused:
            return
        self._paused = False
        self._add_reader(self._sock_fd, self._read_ready)
        if self._loop.get_debug():
            log.debug("%r: resumes reading", self)


    def _read_ready(self) -> None:
        log.debug("%r: _read_ready", self)
        while not self._conn_lost:
            nb = lib.gnutls_record_recv(self._session,
                    ffi.from_buffer(_read_buffer), len(_read_buffer))
            log.debug("%r:  read -> nb=%d", self, nb)
            if nb > 0:
                self._protocol.data_received(bytes(_read_buffer[:nb]))
                if nb == len(_read_buffer):
                    # if _read_buffer is full, then we need to do another
                    # recv(), because we may have a deadlock if we still have
                    # incoming data buffered by gnutls
                    continue
            elif nb == lib._GNUTLS_E_AGAIN or nb == lib._GNUTLS_E_INTERRUPTED:
                pass
            elif nb == 0:
                if self._loop.get_debug():
                    log.debug("%r: received EOF", self)

                # NOTE: we distrust the result of
                # asyncio.StreamReaderProtocol.eof_received() because it
                # assumes that TLS transports do not support .write_eof().
                #
                # This is hardcoded in the stdlib and core devs won't fix it
                # because streams are considered internal:
                #  -> https://bugs.python.org/issue38737
                #
                # Also asyncio streams may be superseded in the future, so
                # let's just wait and see:
                # -> https://bugs.python.org/issue38242
                # -> https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/#the-curious-effectiveness-of-curio
                #
                keep_open = (self._protocol.eof_received()
                        or isinstance(self._protocol, asyncio.StreamReaderProtocol))
                if keep_open and self._can_write_eof:
                    # FIXME: we should keep a reader callback to allow receiving
                    # TLS alerts
                    self._loop._remove_reader(self._sock_fd)
                else:
                    self.close()
            elif nb == lib._GNUTLS_E_PREMATURE_TERMINATION:
                # we silently ignore premature termination errors because many
                # implementations never terminate their TLS session properly
                log.debug("%r: premature termination", self)
                self.abort()
            else:
                self._fatal_error(_make_error(nb),
                        'Fatal read error on Gnutls transport')
            return

    def write(self, data: bytes) -> None:
        log.debug("%r: write %d bytes", self, len(data))

        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError('data: expecting a bytes-like instance, '
                            'got %s' % type(data).__name__)
        if self._eof_written:
            raise RuntimeError('Cannot call write() after write_eof()')
        if not data:
            return

        if self._conn_lost:
            if self._conn_lost >= LOG_THRESHOLD_FOR_CONNLOST_WRITES:
                log.warning('GnutlsTransport: write() after connection_lost.')
            self._conn_lost += 1
            return

        if not self._buffer:
            # Optimization: try to send now.
            nb = lib.gnutls_record_send(self._session,
                    ffi.from_buffer(data), len(data))
            log.debug("%r:  write -> nb=%d", self, nb)

            if nb == lib._GNUTLS_E_AGAIN or nb == lib._GNUTLS_E_INTERRUPTED:
                pass
            elif nb < 0:
                self._fatal_error(_make_error(nb),
                        'Fatal write error on Gnutls transport')
            else:
                data = data[nb:]
                if not data:
                    return

            # Not all was written; register write handler.
            self._loop._add_writer(self._sock_fd, self._write_ready)
            
        # Add it to the buffer.
        self._buffer.extend(data)
        self._maybe_pause_protocol()


    def _write_ready(self) -> None:
        log.debug("%r: write ready (%d bytes)", self, len(self._buffer))
        assert self._buffer, 'Data should not be empty'

        if self._conn_lost:
            return

        nb = lib.gnutls_record_send(self._session,
                ffi.from_buffer(self._buffer), len(self._buffer))
        log.debug("%r:  write -> nb=%d", self, nb)

        if nb == lib._GNUTLS_E_AGAIN or nb == lib._GNUTLS_E_INTERRUPTED:
            return
        elif nb < 0:
            self._loop._remove_writer(self._sock_fd)
            self._buffer.clear()
            self._fatal_error(_make_error(nb),
                    'Fatal write error on Gnutls transport')
        else:
            if nb:
                del self._buffer[:nb]
            self._maybe_resume_protocol()  # May append to buffer.

            if not self._buffer:
                self._loop._remove_writer(self._sock_fd)
                if self._closing:
                    self._shutdown_request = lib.GNUTLS_SHUT_RDWR
                    self._shutdown()
                elif self._eof_written and self._shutdown_request is None:
                    self._shutdown_request = lib.GNUTLS_SHUT_WR
                    self._shutdown()

    def write_eof(self) -> None:
        log.debug("%r: write eof", self)
        if not self._can_write_eof:
            raise NotImplementedError("GnutlsContext.can_write_eof is false")
        if self._closing or self._eof_written:
            return
        self._eof_written = True
        if not self._buffer and self._shutdown_request is None:
            self._shutdown_request = lib.GNUTLS_SHUT_WR
            self._shutdown()

    def can_write_eof(self) -> bool:
        return self._can_write_eof

    def _shutdown(self) -> None:
        how = self._shutdown_request
        log.debug("%r: _shutdown %s", self, how)
        assert how in (lib.GNUTLS_SHUT_WR, lib.GNUTLS_SHUT_RDWR)

        def fatal(err):
            log.debug("%r: -> error", self)
            _unregister_fd_events(self._loop, self._sock_fd)
            self._fatal_error(_make_error(err),
                    'Fatal shutdown error on Gnutls transport')

        err = lib.gnutls_bye(self._session, how)

        if how == lib.GNUTLS_SHUT_WR:
            # just sending eof
            if err == lib._GNUTLS_E_SUCCESS:
                log.debug("%r: -> success", self)
                self._loop._remove_writer(self._sock_fd)
            elif err == lib._GNUTLS_E_AGAIN or err == lib._GNUTLS_E_INTERRUPTED:
                log.debug("%r: -> again", self)
                self._loop._add_writer(self._sock_fd, self._shutdown)
            else:
                fatal(err)
        else:
            # bidirectional shutdown
            if err == lib._GNUTLS_E_SUCCESS:
                log.debug("%r: -> success", self)
                _unregister_fd_events(self._loop, self._sock_fd)
                self._call_connection_lost(None)
            elif err == lib._GNUTLS_E_AGAIN or err == lib._GNUTLS_E_INTERRUPTED:
                log.debug("%r: -> again", self)
                _register_fd_events(self._loop, self._sock_fd, self._session,
                        self._shutdown)
            else:
                fatal(err)


    def close(self) -> None:
        log.debug("%r: close", self)
        if self._closing:
            return
        self._closing = True
        self._loop._remove_reader(self._sock_fd)
        if not self._buffer:
            self._conn_lost += 1
            self._loop._remove_writer(self._sock_fd)
            self._shutdown_request = lib.GNUTLS_SHUT_RDWR
            self._shutdown()


    def abort(self) -> None:
        log.debug("%r: abort", self)
        super().abort()
