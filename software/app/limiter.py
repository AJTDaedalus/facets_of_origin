"""Shared rate limiter instance.

Import this module to access the singleton ``limiter`` object and attach it
to the FastAPI application in ``main.py``.  Individual route modules import
``limiter`` to apply ``@limiter.limit()`` decorators.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
