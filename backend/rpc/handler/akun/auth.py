from rpc.gen.akun import AuthService
from entities.user import User, UserRole

class AuthServiceHandler(AuthService.Iface):
	def __init__(self):
		pass

	def login(self, username, password):
		pass

	def refresh_auth(self, auth_token, refresh_token):
		pass

	def get_user(self, auth_token):
		pass