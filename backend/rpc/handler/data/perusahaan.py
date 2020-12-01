from rpc.gen.data.perusahaan.services import TDataPerusahaanService

from rpc.gen.user.user.types.ttypes import TUserRole
from converter.perusahaan import staging_to_rpc

from models import models

class TDataPerusahaanServiceHandler(TDataPerusahaanService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.perusahaan_model = models['perusahaan']

    def fetch(self, auth_token, query=None):
        auth_payload = self.auth_model.decode_auth(auth_token)
        perusahaans = self.perusahaan_model.fetch(query)
        return [staging_to_rpc(x) for x in perusahaans]

    def get(self, auth_token, perusahaan_id):
        auth_payload = self.auth_model.decode_auth(auth_token)
        return staging_to_rpc(self.perusahaan_model.get(perusahaan_id))

    def create(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        perusahaan = self.perusahaan_model.create(form)
        self.perusahaan_model.commit()
        return staging_to_rpc(perusahaan)

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
