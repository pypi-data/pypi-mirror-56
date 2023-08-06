#!/usr/bin/python3

import ssl as _ssl
from ssl import Purpose, VerifyMode, CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED,\
                DER_cert_to_PEM_cert, PEM_cert_to_DER_cert

import aio_gnutls_transport as _aio_gnutls_transport


def _unimplement_attributes(dct):
    class NotImplemented:
        def __get__(self, instance, owner):
            raise NotImplementedError
        def __set__(self, instance, value):
            raise NotImplementedError
        def __delete__(self, instance):
            raise NotImplementedError

    not_implemented = NotImplemented()
    for name in dir(_ssl.SSLContext()):
        if (name not in ("check_hostname", "verify_mode")
                and not name.startswith("__")
                and not hasattr(_aio_gnutls_transport.GnutlsContext, name)):
            dct[name] = not_implemented


class SSLContext(_aio_gnutls_transport.GnutlsContext,_ssl.SSLContext):
    # NOTE: we need our SSLContext to inherit from the official ssl.SSLContext
    # because some libraries (eg: aiohttp) performe strict type checking.
    #
    # Since we cover only a minimal subset of SSLContext, the likelihood of
    # misconfiguration is real. Therefore we deliberately raise NotImplementedError
    # when the user attempts to use an unsupported method or property
    _unimplement_attributes(locals())

    def __new__(cls) -> "SSLContext":
        self = _ssl._SSLContext.__new__(cls, _ssl.PROTOCOL_TLS)
        self.verify_mode = CERT_NONE
        self.check_hostname = False
        return self

    def _gnutls_cert_required(self) -> bool:
        return self.verify_mode == CERT_REQUIRED

    def _gnutls_verify_cert(self) -> bool:
        return self.verify_mode != CERT_NONE

    def _gnutls_check_hostname(self) -> bool:
        return self.check_hostname

    def __setattr__(self, name, value):
        if (name == "verify_mode" and value == CERT_NONE
                and getattr(self, "check_hostname", True)):
            raise ValueError("Cannot set verify_mode to CERT_NONE when check_hostname is enabled.")

        super().__setattr__(name, value)

# Default GNUTLS priority is "SECURE:-RSA:%PROFILE_MEDIUM:%SERVER_PRECEDENCE"
#
# see:
#   https://www.gnutls.org/manual/html_node/Priority-Strings.html
#   https://www.gnutls.org/manual/html_node/Supported-ciphersuites.html
#
def create_default_context(purpose=Purpose.SERVER_AUTH, *,
        cafile=None, capath=None, cadata=None):

    context = SSLContext()
    context.gnutls_set_priority(_aio_gnutls_transport.DEFAULT_PRIORITY)

    if purpose == Purpose.SERVER_AUTH:
        # verify certs and host name in client mode
        context.verify_mode = CERT_REQUIRED
        context.check_hostname = True

    elif purpose == Purpose.CLIENT_AUTH:
        # FIXME: single use keys do not seem to be available in gnutls
        # Use single use keys in order to improve forward secrecy
#        context.options |= getattr(_ssl, "OP_SINGLE_DH_USE", 0)
#        context.options |= getattr(_ssl, "OP_SINGLE_ECDH_USE", 0)
        pass

    if cafile or capath or cadata:
        context.load_verify_locations(cafile, capath, cadata)
    elif context.verify_mode != CERT_NONE:
        # NOTE: the ssl module calls context.load_default_certs(purpose)
        # but gnutls does not make a difference between server and client
        # certificates when loading the default certificates
        context.load_default_certs()
        
    return context

