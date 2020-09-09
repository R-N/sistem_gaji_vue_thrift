from rpc.gen.akun.user import TUserService
from models import get_model
from rpc.gen.akun.auth.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.akun.user.ttypes import TUser

class TUserServiceHandler(TUserService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def get_user(self, auth_token):
        auth_payload = self.auth_model.decode_auth(auth_token)
        user = self.user_model.get_user(auth_payload['username'])
        if not user:
            raise TAuthError(TAuthErrorCode.AUTH_TOKEN_INVALID)
        return TUser(id=user.id, name=user.name, email=user.email, role=user.role)