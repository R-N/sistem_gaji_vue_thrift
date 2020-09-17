from dotenv import load_dotenv
from .base_key import BaseKeyModel
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()

class GeneralKeyModel(BaseKeyModel):
    def __init__(
        self,
        enc_file,
        dec_file,
        secret,
        expiration,
        enc=None,
        dec=None
    ):
        super(GeneralKeyModel, self).__init__(
            enc_file,
            dec_file,
            secret,
            expiration,
            enc=enc,
            dec=dec
        )

    def make_issuer(self, func):
        return "%s/%s" % (self.secret, func)

    def encode(self, func, ip, payload, expiration=None, now=None):
        payload['iss'] = self.make_issuer(func)
        if ip:
            payload['aud'] = ip
        expiration = expiration or self.expiration
        return super(GeneralKeyModel, self).encode(payload, expiration, now=now)

    def decode(self, func, ip, token):
        return super(GeneralKeyModel, self).decode(
            token,
            issuer=self.make_issuer(func),
            audience=ip
        )
