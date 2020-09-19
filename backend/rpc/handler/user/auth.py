from rpc.gen.user.auth.services import TUserAuthService
from rpc.gen.user.auth.structs.ttypes import TLoginResult

from models import get_model

class TUserAuthServiceHandler(TUserAuthService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def login(self, username, password):
        return TLoginResult(*self.auth_model.login(username, password))

    def refresh_auth(self, auth_token, refresh_token):
        return self.auth_model.refresh_auth(auth_token, refresh_token)

        