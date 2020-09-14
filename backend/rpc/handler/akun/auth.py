from rpc.gen.akun.auth import TAuthService
from models import get_model
from rpc.gen.akun.auth.ttypes import TLoginResult

class TAuthServiceHandler(TAuthService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def login(self, username, password):
        return TLoginResult(*self.auth_model.login(username, password))

    def refresh_auth(self, auth_token, refresh_token):
        return self.auth_model.refresh_auth(auth_token, refresh_token)

    def reset_password(self, email):
        pass

    def send_username(self, email):
        pass
        