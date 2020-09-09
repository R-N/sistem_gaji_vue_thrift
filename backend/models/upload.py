from rpc.gen.file.file.ttypes import TFileError, TFileErrorCode
from datetime import timedelta
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from utils.crypto import encode_jwt, decode_jwt
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

UPLOAD_ENC_FILE = os.getenv("UPLOAD_ENC")
UPLOAD_DEC_FILE = os.getenv("UPLOAD_DEC")
UPLOAD_SECRET = os.getenv("UPLOAD_SECRET")
UPLOAD_EXPIRATION = timedelta(minutes=int(os.getenv("UPLOAD_EXPIRATION_MINUTE") or "30"))

class UploadModel:
    def __init__(
        self,
        upload_enc=None,
        upload_dec=None,
        upload_secret=UPLOAD_SECRET,
        upload_expiration=UPLOAD_EXPIRATION
    ):
        if (not upload_enc) != (not upload_dec):
            raise Exception("Please provide both upload_enc and upload_dec or neither")

        if upload_enc and upload_dec:
            self.set_upload(upload_enc, upload_dec)
        else:
            self.read_upload()

        self.upload_secret = upload_secret
        self.upload_expiration = upload_expiration


    def read_upload(self):
        with open(UPLOAD_ENC_FILE, "r") as f:
            upload_enc = f.read()
        with open(UPLOAD_DEC_FILE, "r") as f:
            upload_dec = f.read()
        self.set_upload(upload_enc, upload_dec)
        
    def set_upload(self, upload_enc, upload_dec):
        self.upload_enc, self.upload_dec = upload_enc, upload_dec
