from datetime import timedelta
import os
import jwt
from dotenv import load_dotenv

from rpc.gen.file.upload.errors.ttypes import TUploadError, TUploadErrorCode

from .general_key import GeneralKeyModel
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()
ENC_FILE = os.getenv("UPLOAD_ENC")
DEC_FILE = os.getenv("UPLOAD_DEC")
SECRET = os.getenv("UPLOAD_SECRET")
EXPIRATION = timedelta(minutes=int(os.getenv("UPLOAD_EXPIRATION_MINUTE") or "30"))

class UploadModel(GeneralKeyModel):
    def __init__(
        self,
        secret=SECRET,
        expiration=EXPIRATION,
        enc=None,
        dec=None,
    ):
        super(UploadModel, self).__init__(
            ENC_FILE,
            DEC_FILE,
            secret,
            expiration,
            enc=enc,
            dec=dec
        )

    def decode(self, func, ip, token):
        try:
            return super(UploadModel, self).decode(func, ip, token)
        except jwt.ExpiredSignatureError:
            raise TUploadError(TUploadErrorCode.UPLOAD_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TUploadError(TUploadErrorCode.UPLOAD_TOKEN_INVALID)

