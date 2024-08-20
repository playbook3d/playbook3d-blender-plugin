import bpy
import webbrowser
import asyncio
from hashlib import sha256
from base64 import urlsafe_b64encode
from urllib.parse import urlencode, urljoin
from contextlib import asynccontextmanager
from time import time


PORT = 8181
HOST = "localhost"
RESPONSE_TYPE = "code"
CODE_CHALLENGE_METHOD = "S256"
CODE_LENGTH = 128  # PKCE spec is between 43 and 128
STATE_LENGTH = 128  # OAuth2 spec doesn't recommend a length, so this is a secure length
import base64

from random import SystemRandom

_sysrand = SystemRandom()

def generate_pkce_pair():
    # Create a cryptographically random url-safe string of PKCE-compliant length.
    # 96 bytes are needed to create 128 characters, the maximum PKCE allows

    new_code_verifier = token_urlsafe(96)[:CODE_LENGTH]

    # PKCE code challenges are encrypted code verifiers.
    # sha256 takes bytes, so we encode the string first, encrypt the bytes,
    # then digest the hash back into bytes

    code_challenge_bytes = sha256(new_code_verifier.encode("ascii")).digest()

    # If the number of bytes aren't a multiple of 3, encoding in base 64 pads the end of the string with `=`
    # Remove any padding (since it's not a valid PKCE code verifier character) and decode it back into a string

    new_code_challenge = urlsafe_b64encode(code_challenge_bytes).rstrip(b"=").decode("ascii")
    return new_code_verifier, new_code_challenge

def token_bytes(nbytes=None):
    """Return a random byte string containing *nbytes* bytes.

    If *nbytes* is ``None`` or not supplied, a reasonable
    default is used.

    >>> token_bytes(16)  #doctest:+SKIP
    b'\\xebr\\x17D*t\\xae\\xd4\\xe3S\\xb6\\xe2\\xebP1\\x8b'

    """
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    return _sysrand.randbytes(nbytes)


def token_urlsafe(nbytes=None):
    """Return a random URL-safe text string, in Base64 encoding.

    The string has *nbytes* random bytes.  If *nbytes* is ``None``
    or not supplied, a reasonable default is used.

    >>> token_urlsafe(16)  #doctest:+SKIP
    'Drmhze6EPcv0fN_81Bj-nA'

    """
    tok = token_bytes(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')


class RbxOAuth2Client:
    _instance = None
    token_data = {}


    def __new__(cls, *args, **kwargs):
        # Makes this class into a singleton
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, rbx):
        self.rbx = rbx


    async def login(self):
        """
        Starts the OAuth2 authorization flow by generating necessary security parameters and
        opening the auth URL in a web browser. Starts a local server listening for the user to be redirected
        back to it after authorizing the requested scopes. Populates token_data if successful, otherwise raises an exception.
        """
        async with self.__set_is_processing_login():
            # from . import auth_callback_request_handler

            from . import event_loop, constants

            # asyncio.set_event_loop(event_loop.get_loop())
            import aiohttp.web as web

            app = web.Application()
            app.add_routes([web.get(f"/{constants.RELATIVE_REDIRECT_PATH.lstrip('/')}", handler.handle_request)])
            runner = web.AppRunner(app)

            # Start a web server on a localhost port
            try:
                # await runner.setup()
                site = web.TCPSite(runner, host=HOST, port=PORT)
                print(f"Starting server on {HOST}:{PORT}")
                # await site.start()

                # Open the authorization URL in the user's browser
                webbrowser.open(self.__construct_auth_url(state, code_challenge))

                # Wait for one request to be handled (the callback from the OAuth2 server)
                # await handler.request_handled_event.wait()
            finally:
                # await runner.cleanup()

        
            # if hasattr(handler.request_handled_event, "exception"):
            #     raise LoginError from handler.request_handled_event.exception
            # self.__complete_login(*handler.request_handled_event.login_details)