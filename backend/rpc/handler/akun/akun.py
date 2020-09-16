from rpc.gen.akun.akun import TAkunService
from models import get_model
from rpc.gen.akun.auth.ttypes import TAuthError, TAuthErrorCode, TUserRole
from rpc.gen.akun.user.ttypes import TUser, TUserError, TUserErrorCode
from converter.user import DBUser_TUser

class TAkunServiceHandler(TAkunService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def fetch_akun(self, auth_token, query):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_users = self.user_model.fetch_users(query)
        return [DBUser_TUser(u) for u in db_users]

    def register_akun(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.register_user(auth_payload['role'], form)
        return DBUser_TUser(db_user)

    def set_role(self, auth_token, user_id, new_role):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        self.user_model.set_role(auth_payload['role'], user_id, new_role)


    def set_email(self, auth_token, user_id, new_email):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        self.user_model.set_email(auth_payload['role'], user_id, new_email)

    def set_password(self, auth_token, user_id, new_password):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        self.user_model.set_password(auth_payload['role'], user_id, new_password)

    def set_enabled(self, auth_token, user_id, new_enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        self.user_model.set_enabled(auth_payload['role'], user_id, new_enabled)
