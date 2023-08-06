#!/usr/bin/python3

from   contextlib import contextmanager
import ssl as native_ssl
from   ssl import Purpose, CERT_REQUIRED, CERT_NONE, CERT_OPTIONAL
from   unittest import TestCase, mock, skipIf

import aio_gnutls_transport.ssl as gnutls_ssl
from   aio_gnutls_transport import ffi, lib, GnutlsContext, GnutlsError
from   .test_common import PY36, EnsureNoTestOverride, patch_lib


class _ContextTestCaseMixin(EnsureNoTestOverride):

    def create_context(self, *k, **kw):
        return self.ssl.SSLContext(*k, **kw)

    def create_default_context(self, *k, **kw):
        return self.ssl.create_default_context(*k, **kw)

    def patch_context(self, *k, **kw):
        return mock.patch.object(self.ssl.SSLContext, *k, **kw)

    def test_default_client_context(self):

        def test(*k):
            with self.patch_context("load_default_certs") as m:
                ctx = self.create_default_context(*k)
                m.assert_called()

            self.assertEqual(ctx.verify_mode, CERT_REQUIRED)
            self.assertEqual(ctx.check_hostname, True)

        test()
        test(Purpose.SERVER_AUTH)

    def test_default_server_context(self):
        with self.patch_context("load_default_certs") as m:
            ctx = self.create_default_context(Purpose.CLIENT_AUTH)
            m.assert_not_called()
        self.assertEqual(ctx.verify_mode, CERT_NONE)
        self.assertEqual(ctx.check_hostname, False)


    def test_default_verify_locations(self):
        with  mock.patch.object(
                self.ssl.SSLContext, "load_verify_locations") as m_explicit,\
              mock.patch.object(
                self.ssl.SSLContext, "load_default_certs") as m_default:

            # default client context -> use default CAs
            ctx = self.ssl.create_default_context()
            m_explicit.assert_not_called()
            m_default.assert_called()
            m_default.reset_mock()

            # default server context -> no CAs
            ctx = self.ssl.create_default_context(Purpose.CLIENT_AUTH)
            m_explicit.assert_not_called()
            m_default.assert_not_called()

            # explicit CAs
            for cafile, capath, cadata in [
                    ("foo", None, None),
                    (None, "bar", None),
                    (None, None, "baz"),
                    ("foo", "bar", None),
                    ]:
                kw = dict(cafile=cafile, capath=capath, cadata=cadata)
                with self.subTest(kw):
                    m_default.reset_mock()
                    m_explicit.reset_mock()

                    ctx = self.ssl.create_default_context(**kw)
                    m_default.assert_not_called()
                    m_explicit.assert_called_once_with(cafile, capath, cadata)
                    m_explicit.reset_mock()

                    ctx = self.ssl.create_default_context(Purpose.CLIENT_AUTH, **kw)
                    m_default.assert_not_called()
                    m_explicit.assert_called_once_with(cafile, capath, cadata)

    @skipIf(PY36,"broken becauss py3.6 has stricter checks")
    def test_cert_none_with_check_hostname(self):
        ctx = self.ssl.SSLContext()
        ctx.check_hostname = False
        ctx.verify_mode = CERT_NONE

        ctx.check_hostname = True
        with self.assertRaisesRegex(ValueError,
                "Cannot set verify_mode to CERT_NONE when check_hostname is enabled."):
            ctx.verify_mode = CERT_NONE
class GnutlsContextTestCase(_ContextTestCaseMixin, TestCase):
    ssl = gnutls_ssl

    def test_set_priority(self):

        # call func(*k, **kw) and ensure that the returned context has its
        # ._priority initialised with the given priority string
        def test_priority_init(expected_priority_string: str, func, *k, **kw):
            priority = None
            orig_func = lib.gnutls_priority_init
            def wrapper(ptr, priority_string, err_pos):
                nonlocal priority
                self.assertIs(priority, None, msg="gnutls_priority_init() called twice")
                self.assertEqual(bytes(ffi.buffer(priority_string)).decode(),
                        expected_priority_string)
                priority = ptr[0]
                return orig_func(ptr, priority_string, err_pos)

            with patch_lib("gnutls_priority_init", wrapper) as m:
                ctx = func(*k, **kw)
                self.assertIsNot(priority, None, msg="gnutls_priority_init() not called")
                self.assertIs(ctx._priority, priority)


        DEFAULT = "SECURE:-RSA:%PROFILE_MEDIUM:%SERVER_PRECEDENCE"

        # default priority hardwired in .create_default_context()
        test_priority_init(DEFAULT, self.create_default_context)
        test_priority_init(DEFAULT, self.create_default_context, Purpose.CLIENT_AUTH)
        test_priority_init(DEFAULT, self.create_default_context, Purpose.SERVER_AUTH)

        # default priority at context creation -> None (means Gnutls's default)
        self.assertIs(self.ssl.SSLContext()._priority, None)
        ctx = GnutlsContext()
        self.assertIs(ctx._priority, None)

        # overriding priority with .gnutls_set_priority()
        def set_priority(value):
            ctx.gnutls_set_priority(value)
            return ctx
        test_priority_init("NORMAL", set_priority, "NORMAL")
        test_priority_init("NORMAL:%COMPAT", set_priority, "NORMAL:%COMPAT")
        ctx.gnutls_set_priority(None)
        self.assertIs(ctx._priority, None)

        # malformatted priority string
        self.assertRaisesRegex(GnutlsError,
                "invalid priority string at 'ñéíóéíáó' \\(GNUTLS_E_INVALID_REQUEST\\)",
                ctx.gnutls_set_priority, "NORMAL:ñéíóéíáó")

    def test_verify_mode(self):
        ctx = gnutls_ssl.SSLContext()
        self.assertEqual(ctx._gnutls_verify_cert(), False)
        self.assertEqual(ctx._gnutls_cert_required(), False)

        ctx.verify_mode=CERT_NONE
        self.assertEqual(ctx._gnutls_verify_cert(), False)
        self.assertEqual(ctx._gnutls_cert_required(), False)

        ctx.verify_mode=CERT_OPTIONAL
        self.assertEqual(ctx._gnutls_verify_cert(), True)
        self.assertEqual(ctx._gnutls_cert_required(), False)

        ctx.verify_mode=CERT_REQUIRED
        self.assertEqual(ctx._gnutls_verify_cert(), True)
        self.assertEqual(ctx._gnutls_cert_required(), True)

        ctx = self.create_default_context()
        self.assertEqual(ctx._gnutls_verify_cert(), True)
        self.assertEqual(ctx._gnutls_cert_required(), True)

        ctx = self.create_default_context(Purpose.CLIENT_AUTH)
        self.assertEqual(ctx._gnutls_verify_cert(), False)
        self.assertEqual(ctx._gnutls_cert_required(), False)

    @skipIf(PY36, "broken becauss py3.6 has stricter checks")
    def test_check_hostname(self):
        ctx = gnutls_ssl.SSLContext()
        self.assertEqual(ctx._gnutls_check_hostname(), False)

        ctx.check_hostname=False
        self.assertEqual(ctx._gnutls_check_hostname(), False)

        ctx.check_hostname=True
        self.assertEqual(ctx._gnutls_check_hostname(), True)

        ctx = self.create_default_context()
        self.assertEqual(ctx._gnutls_check_hostname(), True)

        ctx = self.create_default_context(Purpose.CLIENT_AUTH)
        self.assertEqual(ctx._gnutls_check_hostname(), False)


    def test_load_default_certs(self):
        with patch_lib("gnutls_certificate_set_x509_system_trust") as m:
            ctx = GnutlsContext()

            # success
            m.return_value = 0
            ctx.load_default_certs()
            m.assert_called_once_with(ctx._cred)

            m.reset_mock()

            # failure
            m.return_value = lib._GNUTLS_E_FILE_ERROR
            self.assertRaisesRegex(GnutlsError, "GNUTLS_E_FILE_ERROR",
                    ctx.load_default_certs)

    def test_load_verify_locations(self):
        with patch_lib("gnutls_certificate_set_x509_trust_file") as m:
            ctx = GnutlsContext()

            # success
            m.return_value = 0
            ctx.load_verify_locations("CAFILE")
            m.assert_called_once_with(
                    ctx._cred, b"CAFILE", lib.GNUTLS_X509_FMT_PEM)

            m.reset_mock()

            # failure
            m.return_value = lib._GNUTLS_E_FILE_ERROR
            self.assertRaisesRegex(GnutlsError, "GNUTLS_E_FILE_ERROR",
                    ctx.load_verify_locations, "CAFILE")

            # other args not implemented
            for k in ((None, "foo", None), (None, None, "bar"), ("foo", "bar", None)):
                self.assertRaises(NotImplementedError,
                        ctx.load_verify_locations, *k)

            # must provide at least one value
            self.assertRaisesRegex(TypeError,
                    "cafile, capath and cadata cannot be all omitted",
                    ctx.load_verify_locations)

    def test_unimplemented(self):
        # unimplemented GnutlsContext methods
        ctx = GnutlsContext()
        self.assertRaises(NotImplementedError, ctx._gnutls_cert_required)
        self.assertRaises(NotImplementedError, ctx._gnutls_verify_cert)
        self.assertRaises(NotImplementedError, ctx._gnutls_check_hostname)

        ctx = self.ssl.SSLContext()
        #TODO TEST load_verify_locations load_default_certs load_cert_chain

        # unimplemented SSLContext attributes
        for name in """
                _encode_hostname
                _host_flags
                _load_windows_store_certs
                _set_alpn_protocols
                _set_npn_protocols
                _windows_cert_stores
                _wrap_bio
                _wrap_socket
                cert_store_stats
                get_ca_certs
                get_ciphers
                hostname_checks_common_name
                load_dh_params
                maximum_version
                minimum_version
                options
                post_handshake_auth
                protocol
                session_stats
                set_alpn_protocols
                set_ciphers
                set_default_verify_paths
                set_ecdh_curve
                set_npn_protocols
                set_servername_callback
                sni_callback
                sslobject_class
                sslsocket_class
                verify_flags
                wrap_bio
                wrap_socket
                """.split():
            if PY36 and not hasattr(native_ssl.SSLContext, name):
                # skip methods not present in py3.6
                continue
            with self.subTest(name):
                self.assertRaises(NotImplementedError, getattr, ctx, name)
                self.assertRaises(NotImplementedError, setattr, ctx, name, None)
                self.assertRaises(NotImplementedError, hasattr, ctx, name)
                self.assertRaises(NotImplementedError, delattr, ctx, name)

class OpensslContextTestCase(_ContextTestCaseMixin, TestCase):
    ssl = native_ssl

