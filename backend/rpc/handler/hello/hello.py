from rpc.gen.hello import THelloService
from rpc.gen.akun.ttypes import TUserRole
from models import get_model

class THelloServiceHandler(THelloService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')

    def hello_admin_utama(self, auth_token):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        return "Halo, Admin Utama!"
