import six

if six.PY2:
    """ https://urllib3.readthedocs.io/en/latest/user-guide.html#certificate-verification-in-python-2 
    Engage pyopenssl as instructed in urllib3 for python version 2. """
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()

from leanbase.api import configure, await_initialisation, user

await_initialization = await_initialisation

# Version of the leanbase package
__version__ = "1.4.0"

__all__ = [
    'configure',
    'await_initialisation',
    'await_initialization',
    'user'
]