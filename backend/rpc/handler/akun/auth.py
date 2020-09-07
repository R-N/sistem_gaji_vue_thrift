from rpc.gen.akun import AuthService
from entities.user import User, UserRole
from models import get_model
from rpc.gen.akun.ttypes import AuthError, AuthErrorCode

class AuthServiceHandler(AuthService.Iface):
	def __init__(self):
		self.auth_model = get_model('auth')
		self.user_model = get_model('user')

	def login(self, username, password):
		ret = self.auth_model.login(username, password)
		print(ret)
		return ret

	def refresh_auth(self, auth_token, refresh_token):
		return self.auth_model.refresh_auth(auth_token, refresh_token)

	def get_user(self, auth_token):
		auth_payload = self.auth_model.decode_auth(auth_token)
		user = self.user_model.get_user(auth_payload['username'])
		if not user:
			raise AuthError(AuthErrorCode.AUTH_TOKEN_INVALID)
		return user