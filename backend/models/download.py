from rpc.gen.file.download.ttypes import TDownloadError, TDownloadErrorCode
from datetime import timedelta
import os
from utils.crypto import encode_jwt, decode_jwt
import jwt
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS


DOWNLOAD_ENC_FILE = os.getenv("DOWNLOAD_ENC")
DOWNLOAD_DEC_FILE = os.getenv("DOWNLOAD_DEC")
DOWNLOAD_SECRET = os.getenv("DOWNLOAD_SECRET")

DOWNLOAD_EXPIRATION = timedelta(minutes=int(os.getenv("DOWNLOAD_EXPIRATION_MINUTE") or "30"))

class DownloadModel:
    def __init__(
        self,
        download_enc=None,
        download_dec=None,
        download_secret=DOWNLOAD_SECRET,
        download_expiration=DOWNLOAD_EXPIRATION
    ):
        if (not download_enc) != (not download_dec):
            raise Exception("Please provide both download_enc and download_dec or neither")

        if download_enc and download_dec:
            self.set_download(download_enc, download_dec)
        else:
            self.read_download()
        self.download_secret = download_secret
        self.download_expiration = download_expiration


    def read_download(self):
        with open(DOWNLOAD_ENC_FILE, "r") as f:
            download_enc = f.read()
        with open(DOWNLOAD_DEC_FILE, "r") as f:
            download_dec = f.read()
        self.set_download(download_enc, download_dec)

    def set_download(self, download_enc, download_dec):
        self.download_enc, self.download_dec = download_enc, download_dec

    def make_issuer(self, func):
        return "%s/%s" % (self.download_secret, func)

    def encode(self, ip, func, file_name):
        download_payload = {
            'file_name': file_name,
            'iss': self.make_issuer(func),
            'aud': ip
        }
        return encode_jwt(download_payload, self.download_enc, self.download_expiration)

    def decode(self, ip, func, token):
        try:
            return decode_jwt(token, self.download_dec, issuer=self.make_issuer(func), audience=ip)
        except jwt.ExpiredSignatureError:
            raise TDownloadError(TDownloadErrorCode.DOWNLOAD_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TDownloadError(TDownloadErrorCode.DOWNLOAD_TOKEN_INVALID)
