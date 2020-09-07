from rpc.gen.akun.ttypes import UserRole, User as BaseUser

class User(BaseUser):
	def __init__(self, name=None, role=None):
		super(name, role)