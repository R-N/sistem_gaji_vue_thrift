from flask import request

from rpc.gen.user.profile.services import TUserProfileService
from rpc.gen.user.auth.structs.ttypes import TLoginResult
from rpc.gen.user.auth.errors.ttypes import TLoginError, TLoginErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole

from models import models
from converter.user import db_to_rpc

class TUserProfileServiceHandler(TUserProfileService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']
        self.email_model = models['email']

    def get_user(self, auth_token):
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_by_id(auth_payload['user_id'])
        return db_to_rpc(db_user)

    def change_email(self, auth_token, new_email):
        ip = request.remote_addr
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_by_id(auth_payload['user_id'])
        self.email_model.send_change_email(ip, db_user, new_email)
        self.user_model.commit()

    def set_password(self, auth_token, old_password, new_password):
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_by_id(auth_payload['user_id'])
        if not db_user.verify_password(old_password):
            raise TLoginError(TLoginErrorCode.PASSWORD_SALAH)
        self.user_model.set_password(TUserRole.SUPER_ADMIN, db_user, new_password)
        self.email_model.send_change_password_succeeded(db_user)
        auth_token, refresh_token = self.auth_model.make_pair(user=db_user)
        self.user_model.commit()
        return TLoginResult(auth_token, refresh_token)

    def set_name(self, auth_token, new_name):
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_by_id(auth_payload['user_id'])
        self.user_model.set_name(TUserRole.SUPER_ADMIN, db_user, new_name)
        self.user_model.commit()
