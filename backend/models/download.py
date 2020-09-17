from rpc.gen.file.download.ttypes import TDownloadError, TDownloadErrorCode
from datetime import timedelta
import os
import jwt
from dotenv import load_dotenv
from .general_key import GeneralKeyModel
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()
ENC_FILE = os.getenv("DOWNLOAD_ENC")
DEC_FILE = os.getenv("DOWNLOAD_DEC")
SECRET = os.getenv("DOWNLOAD_SECRET")

EXPIRATION = timedelta(minutes=int(os.getenv("DOWNLOAD_EXPIRATION_MINUTE") or "30"))

class DownloadModel(GeneralKeyModel):
    def __init__(
        self,
        secret=SECRET,
        expiration=EXPIRATION,
        enc=None,
        dec=None
    ):
        super(DownloadModel, self).__init__(
            ENC_FILE,
            DEC_FILE,
            secret,
            expiration,
            enc=enc,
            dec=dec
        )

    def decode(self, func, ip, token):
        try:
            return super(DownloadModel, self).decode(func, ip, token)
        except jwt.ExpiredSignatureError:
            raise TDownloadError(TDownloadErrorCode.DOWNLOAD_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TDownloadError(TDownloadErrorCode.DOWNLOAD_TOKEN_INVALID)
