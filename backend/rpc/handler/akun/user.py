from rpc.gen.akun.user import TUserService
from models import get_model
from rpc.gen.akun.auth.ttypes import TAuthError, TAuthErrorCode, TLoginResult
from converter.user import DBUser_TUser

class TUserServiceHandler(TUserService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def get_user(self, auth_token):
        auth_payload = self.auth_model.decode_auth(auth_token)
        db_user = self.user_model.get_user(auth_payload['user_id'])
        return DBUser_TUser(db_user)

    def set_email(self, auth_token, new_email):
        auth_payload = self.auth_model.decode_auth(auth_token)
        self.user_model.set_email(auth_payload['role'], auth_payload['user_id'], new_email)

    def set_password(self, auth_token, new_password):
        auth_payload = self.auth_model.decode_auth(auth_token)
        user_id = auth_payload['user_id']
        self.user_model.set_password(auth_payload['role'], user_id, new_password)
        user = self.user_model.get_user(user_id)
        return TLoginResult(*self.auth_model.make_pair(user=user))

    def set_name(self, auth_token, new_name):
        auth_payload = self.auth_model.decode_auth(auth_token)
        self.user_model.set_name(auth_payload['role'], auth_payload['user_id'], new_name)
