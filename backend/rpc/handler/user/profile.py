from flask import request

from rpc.gen.user.profile.services import TUserProfileService
from rpc.gen.user.auth.structs.ttypes import TLoginResult
from rpc.gen.user.auth.errors.ttypes import TLoginError, TLoginErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole

from models import get_model
from converter.user import DBUser_TUser

class TUserProfileServiceHandler(TUserProfileService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def get_user(self, auth_token):
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_user(auth_payload['user_id'])
        return DBUser_TUser(db_user)

    def change_email(self, auth_token, new_email):
        ip = request.remote_addr
        auth_payload = self.auth_model.decode_auth(auth_token)
        self.user_model.send_change_email(ip, TUserRole.SUPER_ADMIN, auth_payload['user_id'], new_email)

    def set_password(self, auth_token, old_password, new_password):
        auth_payload = self.auth_model.decode_auth(auth_token)
        user_id = auth_payload['user_id']
        user = self.user_model.get_user(user_id)
        if not user.verify_password(old_password):
            raise TLoginError(TLoginErrorCode.PASSWORD_SALAH)
        self.user_model.set_password(user_id, new_password)
        user = self.user_model.get_user(user_id)
        return TLoginResult(*self.auth_model.make_pair(user=user))

    def set_name(self, auth_token, new_name):
        auth_payload = self.auth_model.decode_auth(auth_token)
        self.user_model.set_name(TUserRole.SUPER_ADMIN, auth_payload['user_id'], new_name)
