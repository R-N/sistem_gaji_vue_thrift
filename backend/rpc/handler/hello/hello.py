from rpc.gen.hello import HelloService
from entities.user import User, UserRole
from models import get_model

class HelloServiceHandler(HelloService.Iface):
	def __init__(self):
		self.auth_model = get_model('auth')

	def hello_admin_utama(self, auth_token):
		auth_payload = self.auth_model.require_role(UserRole.ADMIN_UTAMA)
		return "Halo, Admin Utama!"