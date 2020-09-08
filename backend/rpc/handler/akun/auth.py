from rpc.gen.akun import TAuthService
from models import get_model
from rpc.gen.akun.ttypes import TUser, TLoginResult, TAuthError, TAuthErrorCode

class TAuthServiceHandler(TAuthService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def login(self, username, password):
        return TLoginResult(*self.auth_model.login(username, password))

    def refresh_auth(self, auth_token, refresh_token):
        return self.auth_model.refresh_auth(auth_token, refresh_token)

    def get_user(self, auth_token):
        auth_payload = self.auth_model.decode_auth(auth_token)
        user = self.user_model.get_user(auth_payload['username'])
        if not user:
            raise TAuthError(TAuthErrorCode.AUTH_TOKEN_INVALID)
        return TUser(id=user.id, name=user.name, role=user.role)