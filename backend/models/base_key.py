from utils.crypto import encode_jwt, decode_jwt
from dotenv import load_dotenv
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()

class BaseKeyModel:
    def __init__(
        self,
        enc_file,
        dec_file,
        secret,
        expiration,
        enc=None,
        dec=None
    ):
        if (not enc) != (not dec):
            raise Exception("Please provide both enc and dec or neither")
        self.secret = secret
        self.expiration = expiration
        self.enc_file = enc_file
        self.dec_file = dec_file
        if enc and dec:
            self.set_keys(enc, dec)
        else:
            self.read_keys()

    def read_keys(self):
        with open(self.enc_file, "r") as f:
            enc = f.read()
        with open(self.dec_file, "r") as f:
            dec = f.read()
        self.set_keys(enc, dec)

    def set_keys(self, enc, dec):
        self.enc, self.dec = enc, dec

    def encode(self, payload, expiration=None, now=None):
        expiration = expiration or self.expiration
        return encode_jwt(payload, self.enc, expiration, now=now)

    def decode(self, token, issuer=None, audience=None):
        return decode_jwt(token, self.dec, issuer=issuer, audience=audience)
