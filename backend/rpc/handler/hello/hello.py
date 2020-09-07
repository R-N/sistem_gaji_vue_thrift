from rpc.gen.hello import HelloService
from entities.user import User, UserRole

class HelloServiceHandler(HelloService.Iface):
	def __init__(self):
		pass

	def hello_admin_utama(self, auth_token):
		pass