import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils.crypto import md5

from rpc.gen.user.auth.errors.ttypes import TLoginError, TLoginErrorCode, TAuthError, TAuthErrorCode
from rpc.gen.user.user.types.constants import T_USER_ROLE_DOUBLES
from db.entities.general import DbUser

import db

from .basic.base_key import BaseKeyModel
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()

AUTH_ENC_FILE = os.getenv("AUTH_ENC")
AUTH_DEC_FILE = os.getenv("AUTH_DEC")
AUTH_SECRET = os.getenv("AUTH_SECRET")
REFRESH_ENC_FILE = os.getenv("REFRESH_ENC")
REFRESH_DEC_FILE = os.getenv("REFRESH_DEC")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")

AUTH_EXPIRATION = timedelta(minutes=int(os.getenv("AUTH_EXPIRATION_MINUTE") or "12"))
REFRESH_EXPIRATION = timedelta(minutes=int(os.getenv("REFRESH_EXPIRATION_MINUTE") or "1440"))


class AuthModel:
    def __init__(
        self,
        auth_secret=AUTH_SECRET,
        refresh_secret=REFRESH_SECRET,
        auth_expiration=AUTH_EXPIRATION,
        refresh_expiration=REFRESH_EXPIRATION,
        auth_enc=None,
        auth_dec=None,
        refresh_enc=None,
        refresh_dec=None
    ):
        if (not auth_enc) != (not auth_dec):
            raise Exception("Please provide both auth_enc and auth_dec or neither")
        if (not refresh_enc) != (not refresh_dec):
            raise Exception("Please provide both refresh_enc and refresh_dec or neither")

        self.auth_key_model = BaseKeyModel(
            AUTH_ENC_FILE,
            AUTH_DEC_FILE,
            secret=auth_secret,
            expiration=auth_expiration,
            enc=auth_enc,
            dec=auth_dec
        )
        self.refresh_key_model = BaseKeyModel(
            REFRESH_ENC_FILE,
            REFRESH_DEC_FILE,
            secret=refresh_secret,
            expiration=refresh_expiration,
            enc=refresh_enc,
            dec=refresh_dec
        )

    @property
    def auth_secret(self):
        return self.auth_key_model.secret

    @property
    def refresh_secret(self):
        return self.refresh_key_model.secret
    

    def encode_auth(self, payload, now=None):
        return self.auth_key_model.encode(payload, now=now)

    def decode_auth(self, token):
        try:
            return self.auth_key_model.decode(token, issuer=self.auth_secret)
        except jwt.ExpiredSignatureError:
            raise TAuthError(TAuthErrorCode.AUTH_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TAuthError(TAuthErrorCode.AUTH_TOKEN_INVALID)

    def encode_refresh(self, payload, now=None):
        return self.refresh_key_model.encode(payload, now=now)

    def decode_refresh(self, token, auth_secret_2):
        try:
            return self.refresh_key_model.decode(
                token,
                issuer=self.refresh_secret,
                audience=auth_secret_2
            )
        except jwt.ExpiredSignatureError:
            raise TLoginError(TLoginErrorCode.REFRESH_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TLoginError(TLoginErrorCode.REFRESH_TOKEN_INVALID)

    def make_pair(self, user, now=None, auth_payload=None):
        if not auth_payload:
            auth_payload = {}
        auth_payload.update({
            'user_id': user.id,
            'role': user.role,
            'iss': self.auth_secret
        })
        
        now = now or datetime.utcnow()
        user_id = auth_payload['user_id']
        user_id_str = str(user_id)
        now_ts = str(now.timestamp())

        auth_payload['auth_secret_2'] = md5(user_id_str + 'uauth' + now_ts + self.auth_secret)
        auth_token = self.encode_auth(auth_payload, now=now)

        refresh_secret_2 = md5(user_id_str + 'urefresh' + now_ts + self.refresh_secret)

        user.refresh_secret_2 = refresh_secret_2
        db.session.add(user)
        #db.commit()

        refresh_payload = {
            'iss': self.refresh_secret,
            'aud': auth_payload['auth_secret_2'],
            'refresh_secret_2': refresh_secret_2
        }
        refresh_token = self.encode_refresh(refresh_payload, now=now)
        return auth_token, refresh_token

    def login(self, user, password):
        if not password:
            raise TLoginError(TLoginErrorCode.PASSWORD_EMPTY)
        if not user.verified:
            raise TLoginError(TLoginErrorCode.USER_UNVERIFIED)
        if not user.verify_password(password):
            raise TLoginError(TLoginErrorCode.USERNAME_PASSWORD_SALAH)
        if not user.enabled:
            raise TLoginError(TLoginErrorCode.USER_DISABLED)

        return self.make_pair(user)

    def refresh_auth(self, user, auth_payload, refresh_token):
        refresh_payload = self.decode_refresh(refresh_token, auth_payload['auth_secret_2'])

        if not (user and user.verified and user.enabled and user.refresh_secret_2 and user.refresh_secret_2 == refresh_payload['refresh_secret_2']):
            raise TLoginError(TLoginErrorCode.REFRESH_TOKEN_EXPIRED)

        auth_token = self.encode_auth(auth_payload)
        return auth_token

    def require_role(self, actor, roles, Exception=TAuthError, error_code=TAuthErrorCode.ROLE_INVALID):
        if isinstance(actor, str):
            actor = self.decode_auth(actor)
        DbUser.validator().validate_actor_role(actor, roles, Exception=Exception, error_code=error_code)
        return actor
