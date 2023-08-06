import sys
if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version should be 3.7+")

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .actions import Checker, Verdict, CheckRequest, PutRequest, GetRequest
