from rpc.gen.data.departemen.services import TDataDepartemenService
from rpc.gen.data.departemen.structs.ttypes import TDepartemen

from rpc.gen.user.user.types.ttypes import TUserRole

from models import models

class TDataDepartemenServiceHandler(TDataDepartemenService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.departemen_model = models['departemen']

    def fetch(self, auth_token, query=None):
        auth_payload = self.auth_model.decode_auth(auth_token)
        print(query)
        departemens = self.departemen_model.fetch(query)
        return [x.fill(TDepartemen()) for x in departemens]

    def get(self, auth_token, departemen_id):
        auth_payload = self.auth_model.decode_auth(auth_token)
        return self.departemen_model.get(departemen_id).fill(TDepartemen())

    def create(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        print(form)
        departemen = self.departemen_model.create(form)
        self.departemen_model.commit()
        return departemen.fill(TDepartemen())

    def set_enabled(self, auth_token, departemen_id, enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        departemen = self.departemen_model.get(departemen_id)
        self.departemen_model.set_enabled(departemen, enabled)
        self.departemen_model.commit()

    def set_nama(self, auth_token, departemen_id, nama):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        departemen = self.departemen_model.get(departemen_id)
        self.departemen_model.set_nama(departemen, nama)
        self.departemen_model.commit()
