from rpc.gen.data.job_level.services import TDataJobLevelService
from rpc.gen.data.job_level.structs.ttypes import TJobLevel

from rpc.gen.user.user.types.ttypes import TUserRole

from models import models

class TDataJobLevelServiceHandler(TDataJobLevelService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.job_level_model = models['job_level']

    def fetch(self, auth_token, query=None):
        auth_payload = self.auth_model.decode_auth(auth_token)
        job_levels = self.job_level_model.fetch(query)
        return [x.fill(TJobLevel()) for x in job_levels]

    def get(self, auth_token, job_level_id):
        auth_payload = self.auth_model.decode_auth(auth_token)
        return self.job_level_model.get(job_level_id).fill(TJobLevel())

    def create(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.create(form)
        self.job_level_model.commit()
        return job_level.fill(TJobLevel())

    def set_enabled(self, auth_token, job_level_id, enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_enabled(job_level, enabled)
        self.job_level_model.commit()

    def set_nama(self, auth_token, job_level_id, nama):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_nama(job_level, nama)
        self.job_level_model.commit()

    def set_gaji_pokok(self, auth_token, job_level_id, gaji_pokok):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_gaji_pokok(job_level, gaji_pokok)
        self.job_level_model.commit()

    def set_tunjangan_jabatan(self, auth_token, job_level_id, tunjangan_jabatan):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_tunjangan_jabatan(job_level, tunjangan_jabatan)
        self.job_level_model.commit()

    def set_gaji_pokok(self, auth_token, job_level_id, gaji_pokok):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_gaji_pokok(job_level, gaji_pokok)
        self.job_level_model.commit()

    def set_upah_lembur(self, auth_token, job_level_id, upah_lembur):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_upah_lembur(job_level, upah_lembur)
        self.job_level_model.commit()

    def set_upah_lembur_1(self, auth_token, job_level_id, upah_lembur):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_upah_lembur_1(job_level, upah_lembur)
        self.job_level_model.commit()

    def set_upah_lembur_2(self, auth_token, job_level_id, upah_lembur):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_upah_lembur_2(job_level, upah_lembur)
        self.job_level_model.commit()

    def set_upah_lembur_3(self, auth_token, job_level_id, upah_lembur):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        job_level = self.job_level_model.get(job_level_id)
        self.job_level_model.set_upah_lembur_3(job_level, upah_lembur)
        self.job_level_model.commit()
