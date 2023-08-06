#!/usr/bin/python3

import cffi

CONSTANTS = """
GNUTLS_E_SUCCESS
GNUTLS_E_AGAIN
GNUTLS_E_INTERRUPTED
GNUTLS_E_FILE_ERROR
GNUTLS_E_PUSH_ERROR
GNUTLS_E_PULL_ERROR
GNUTLS_E_CERTIFICATE_ERROR
GNUTLS_E_CERTIFICATE_VERIFICATION_ERROR
GNUTLS_E_NO_CERTIFICATE_FOUND
GNUTLS_E_PREMATURE_TERMINATION
""".split()

ffibuilder = cffi.FFI()
ffibuilder.cdef("""

typedef struct {...;} gnutls_session_t;
typedef struct {...;} gnutls_certificate_credentials_t;
typedef struct {...;} gnutls_priority_t;
typedef int gnutls_certificate_verify_function(gnutls_session_t);
typedef struct {
 unsigned char *data;
 unsigned int size;
} gnutls_datum_t;

typedef enum {
 GNUTLS_SERVER = ...,
 GNUTLS_CLIENT = ...,
 GNUTLS_DATAGRAM = ...,
 GNUTLS_NONBLOCK = ...,
 GNUTLS_NO_EXTENSIONS = ...,
 GNUTLS_NO_REPLAY_PROTECTION = ...,
 GNUTLS_NO_SIGNAL = ...,
 GNUTLS_ALLOW_ID_CHANGE = ...,
 GNUTLS_ENABLE_FALSE_START = ...,
 GNUTLS_FORCE_CLIENT_CERT = ...,
 GNUTLS_NO_TICKETS = ...,
 ...
} gnutls_init_flags_t;

typedef enum {
 GNUTLS_SHUT_RDWR = ...,
 GNUTLS_SHUT_WR = ...,
 ...
} gnutls_close_request_t;

typedef enum {
 GNUTLS_X509_FMT_DER = ...,
 GNUTLS_X509_FMT_PEM = ...,
 ...
} gnutls_x509_crt_fmt_t;

typedef enum {
 GNUTLS_CRD_CERTIFICATE = ...,
 GNUTLS_CRD_ANON = ...,
 GNUTLS_CRD_SRP = ...,
 GNUTLS_CRD_PSK = ...,
 GNUTLS_CRD_IA = ...,
 ...
} gnutls_credentials_type_t;

typedef enum {
 GNUTLS_CERT_INVALID = ...,
 GNUTLS_CERT_REVOKED = ...,
 GNUTLS_CERT_SIGNER_NOT_FOUND = ...,
 GNUTLS_CERT_SIGNER_NOT_CA = ...,
 GNUTLS_CERT_INSECURE_ALGORITHM = ...,
 GNUTLS_CERT_NOT_ACTIVATED = ...,
 GNUTLS_CERT_EXPIRED = ...,
 GNUTLS_CERT_SIGNATURE_FAILURE = ...,
 GNUTLS_CERT_REVOCATION_DATA_SUPERSEDED = ...,
 GNUTLS_CERT_UNEXPECTED_OWNER = ...,
 GNUTLS_CERT_REVOCATION_DATA_ISSUED_IN_FUTURE = ...,
 GNUTLS_CERT_SIGNER_CONSTRAINTS_FAILURE = ...,
 GNUTLS_CERT_MISMATCH = ...,
 GNUTLS_CERT_PURPOSE_MISMATCH = ...,
 GNUTLS_CERT_MISSING_OCSP_STATUS = ...,
 GNUTLS_CERT_INVALID_OCSP_STATUS = ...,
 ...
} gnutls_certificate_status_t;

typedef enum gnutls_certificate_verify_flags {
 GNUTLS_VERIFY_DISABLE_CA_SIGN = ...,
// GNUTLS_VERIFY_DO_NOT_ALLOW_IP_MATCHES = ...,
 GNUTLS_VERIFY_DO_NOT_ALLOW_SAME = ...,
 GNUTLS_VERIFY_ALLOW_ANY_X509_V1_CA_CRT = ...,
 GNUTLS_VERIFY_ALLOW_SIGN_RSA_MD2 = ...,
 GNUTLS_VERIFY_ALLOW_SIGN_RSA_MD5 = ...,
 GNUTLS_VERIFY_DISABLE_TIME_CHECKS = ...,
 GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS = ...,
 GNUTLS_VERIFY_DO_NOT_ALLOW_X509_V1_CA_CRT = ...,
 GNUTLS_VERIFY_DISABLE_CRL_CHECKS = ...,
 GNUTLS_VERIFY_ALLOW_UNSORTED_CHAIN = ...,
 GNUTLS_VERIFY_DO_NOT_ALLOW_UNSORTED_CHAIN = ...,
 GNUTLS_VERIFY_DO_NOT_ALLOW_WILDCARDS = ...,
 GNUTLS_VERIFY_USE_TLS1_RSA = ...,
// GNUTLS_VERIFY_IGNORE_UNKNOWN_CRIT_EXTENSIONS = ...,
// GNUTLS_VERIFY_ALLOW_SIGN_WITH_SHA1 = ...,
 ...
} gnutls_certificate_verify_flags;

typedef enum {
 GNUTLS_CERT_IGNORE = ...,
 GNUTLS_CERT_REQUEST = ...,
 GNUTLS_CERT_REQUIRE = ...
} gnutls_certificate_request_t;

typedef enum {
 GNUTLS_CRT_UNKNOWN = ...,
 GNUTLS_CRT_X509 = ...,
 GNUTLS_CRT_OPENPGP = ...,
 ...
} gnutls_certificate_type_t;

typedef enum {
 GNUTLS_NAME_DNS = ...,
 ...
} gnutls_server_name_type_t;

%s

int gnutls_global_init(void);
void gnutls_global_deinit(void);

int gnutls_init (gnutls_session_t * session, unsigned int flags);
void gnutls_deinit (gnutls_session_t session);

void gnutls_free (void*);

int gnutls_set_default_priority (gnutls_session_t session);

int gnutls_priority_init (gnutls_priority_t * priority_cache, const char * priorities, const char ** err_pos);
int gnutls_priority_set (gnutls_session_t session, gnutls_priority_t priority);
void gnutls_priority_deinit (gnutls_priority_t priority_cache);

void gnutls_certificate_server_set_request (gnutls_session_t session, gnutls_certificate_request_t req);

int gnutls_server_name_set (gnutls_session_t session, gnutls_server_name_type_t type, const void * name, size_t name_length);

int gnutls_certificate_verification_status_print (unsigned int status, gnutls_certificate_type_t type, gnutls_datum_t * out, unsigned int flags);

int gnutls_certificate_allocate_credentials (gnutls_certificate_credentials_t * res);
void gnutls_certificate_free_credentials (gnutls_certificate_credentials_t sc);

int gnutls_certificate_set_x509_system_trust (gnutls_certificate_credentials_t cred);
int gnutls_certificate_set_x509_trust_file (gnutls_certificate_credentials_t cred, const char * cafile, gnutls_x509_crt_fmt_t type);

int gnutls_certificate_set_x509_key_file2 (gnutls_certificate_credentials_t res, const char * certfile, const char * keyfile, gnutls_x509_crt_fmt_t type, const char * pass, unsigned int flags);

unsigned int gnutls_certificate_get_verify_flags (gnutls_certificate_credentials_t res);
void gnutls_certificate_set_verify_flags (gnutls_certificate_credentials_t res, unsigned int flags);

void gnutls_session_set_verify_function (gnutls_session_t session, gnutls_certificate_verify_function * func);
const gnutls_datum_t * gnutls_certificate_get_peers (gnutls_session_t session, unsigned int * list_size);
int gnutls_certificate_verify_peers3 (gnutls_session_t session, const char * hostname, unsigned int * status);


int gnutls_credentials_set (gnutls_session_t session, gnutls_credentials_type_t type, void * cred);
void gnutls_session_set_verify_cert (gnutls_session_t session, const char * hostname, unsigned flags);
unsigned int gnutls_session_get_verify_cert_status (gnutls_session_t session);

int gnutls_handshake (gnutls_session_t session);

const char * gnutls_strerror (int error);
const char * gnutls_strerror_name (int error);
void gnutls_transport_set_int (gnutls_session_t session, int fd);

int gnutls_record_get_direction (gnutls_session_t session);
ssize_t gnutls_record_recv(gnutls_session_t session, char* data, ssize_t size);
ssize_t gnutls_record_send(gnutls_session_t session, char* data, ssize_t size);

int gnutls_bye (gnutls_session_t session, gnutls_close_request_t how);


extern "Python" int _aio_gnutls_verify_cert_callback(gnutls_session_t);

""" % "".join("static const int _%s;\n" % name for name in CONSTANTS))

ffibuilder.set_source("aio_gnutls_transport._gnutls",
        "#include <gnutls/gnutls.h>\n#include <gnutls/x509.h>\n" +
        "".join("static const int _%s = %s;\n" % (name, name) for name in CONSTANTS),
        libraries=["gnutls"])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
