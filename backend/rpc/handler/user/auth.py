from rpc.gen.user.auth.services import TUserAuthService
from rpc.gen.user.auth.structs.ttypes import TLoginResult
from rpc.gen.user.auth.errors.ttypes import TLoginError, TLoginErrorCode

from models import models
import db

class TUserAuthServiceHandler(TUserAuthService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']

    def login(self, username, password):
        if not username:
            raise TLoginError(TLoginErrorCode.USERNAME_EMPTY)
        if not password:
            raise TLoginError(TLoginErrorCode.PASSWORD_EMPTY)
        db_user = self.user_model.get_by_username_email_silent(username)
        if not db_user:
            raise TLoginError(TLoginErrorCode.USERNAME_PASSWORD_SALAH)
        auth_token, refresh_token = self.auth_model.login(db_user, password)
        db.commit()
        return TLoginResult(auth_token, refresh_token)

    def refresh_auth(self, auth_token, refresh_token):
        actor = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get(actor['user_id'], actor=actor)
        refresh_token = self.auth_model.refresh_auth(db_user, actor, refresh_token)
        db.commit()
        return refresh_token

        