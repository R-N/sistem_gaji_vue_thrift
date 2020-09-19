from rpc.gen.hello.hello.services import THelloService
from rpc.gen.user.user.types.ttypes import TUserRole

from models import models

class THelloServiceHandler(THelloService.Iface):
    def __init__(self):
        self.auth_model = models['auth']

    def hello_admin_utama(self, auth_token):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        return "Halo, Admin Utama!"
