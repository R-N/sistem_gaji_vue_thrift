from flask import request

from rpc.gen.user.profile.services import TUserProfileService
from rpc.gen.user.auth.structs.ttypes import TLoginResult
from rpc.gen.user.auth.errors.ttypes import TLoginError, TLoginErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.user.structs.ttypes import TUser

from models import models

class TUserProfileServiceHandler(TUserProfileService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']
        self.email_model = models['email']

    def get_user(self, auth_token):
        actor = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get(actor['user_id'], actor=actor)
        return db_user.fill(TUser())

    def change_email(self, auth_token, new_email):
        ip = request.remote_addr
        actor = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get(actor['user_id'])
        self.email_model.send_change_email(ip, db_user, new_email)
        self.user_model.commit()

    def set_password(self, auth_token, old_password, new_password):
        actor = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get(actor['user_id'], actor=actor)
        if not db_user.verify_password(old_password):
            raise TLoginError(TLoginErrorCode.PASSWORD_SALAH)
        self.user_model.set_password(db_user, new_password, actor=TUserRole.SUPER_ADMIN)
        self.email_model.send_change_password_succeeded(db_user)
        auth_token, refresh_token = self.auth_model.make_pair(user=db_user)
        self.user_model.commit()
        return TLoginResult(auth_token, refresh_token)

    def set_name(self, auth_token, new_name):
        actor = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get(actor['user_id'], actor=actor)
        self.user_model.set_name(db_user, new_name, actor=TUserRole.SUPER_ADMIN)
        self.user_model.commit()
