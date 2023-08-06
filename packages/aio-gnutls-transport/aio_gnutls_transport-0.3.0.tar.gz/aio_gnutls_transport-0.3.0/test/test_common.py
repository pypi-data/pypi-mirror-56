#!/usr/bin/python3

from   contextlib import contextmanager
import sys
from   unittest import mock

import aio_gnutls_transport
from   aio_gnutls_transport import lib

PY36 = sys.version_info[:2] < (3,7)

class _MockLib:
    class _Lib:
        locals().update(lib.__dict__)
    _lib = _Lib()
    _count = 0
@contextmanager
def patch_lib(*k, **kw):
    ml = _MockLib
    p_lib = nullcontext() if ml._count else mock.patch.object(aio_gnutls_transport, "lib", ml._lib)

    with p_lib, mock.patch.object(ml._lib, *k, **kw) as m:
        ml._count += 1
        try:
            yield m
        finally:
            ml._count -= 1


class EnsureNoTestOverride:
    """Base class to ensure that no 'test_*' method is reimplemented by any subclass"""
    def __init_subclass__(cls):
        super().__init_subclass__()
        for base in cls.__mro__:
            for key, val in base.__dict__.items():
                if key.startswith("test_"):
                    assert getattr(cls, key) is val, (
                            f"attribute {key!r} is reimplemented by {cls}")

