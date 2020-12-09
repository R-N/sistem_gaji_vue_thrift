from rpc.gen.data.perusahaan.services import TDataPerusahaanService
from rpc.gen.data.perusahaan.structs.ttypes import TPerusahaan

from rpc.gen.user.user.types.ttypes import TUserRole

from models import models

class TDataPerusahaanServiceHandler(TDataPerusahaanService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.perusahaan_model = models['perusahaan']

    def fetch(self, auth_token, query=None):
        auth_payload = self.auth_model.decode_auth(auth_token)
        perusahaans = self.perusahaan_model.fetch(query)
        return [x.fill(TPerusahaan()) for x in perusahaans]

    def get(self, auth_token, perusahaan_id):
        auth_payload = self.auth_model.decode_auth(auth_token)
        return self.perusahaan_model.get(perusahaan_id).fill(TPerusahaan())

    def create(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        perusahaan = self.perusahaan_model.create(form)
        self.perusahaan_model.commit()
        return perusahaan.fill(TPerusahaan())

    def set_enabled(self, auth_token, perusahaan_id, enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        perusahaan = self.perusahaan_model.get(perusahaan_id)
        self.perusahaan_model.set_enabled(perusahaan, enabled)
        self.perusahaan_model.commit()

    def set_nama(self, auth_token, perusahaan_id, nama):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        perusahaan = self.perusahaan_model.get(perusahaan_id)
        self.perusahaan_model.set_nama(perusahaan, nama)
        self.perusahaan_model.commit()
