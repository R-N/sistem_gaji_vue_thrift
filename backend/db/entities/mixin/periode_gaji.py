from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from datetime import date
import rpc.gen.user.user.errors.constants as user_constants


class MxPeriodeGaji:
    __tablename__ = 'periode_gaji'

    @declared_attr
    def periode(cls):
        return Column(Date, primary_key=True)

    @declared_attr
    def terakhir_diubah(cls):
        return Column(Date, nullable=True, default=None)

    @declared_attr
    def pengubah_id(cls):
        return Column(Integer, nullable=False)

    # TODO: Is it possible to have relationship to other schema?

    @declared_attr
    def pengubah_name(cls):
        return Column(String(user_constants.NAME_MAX_LEN), nullable=False)

    @declared_attr
    def job_level_valid(cls):
        return Column(Date, nullable=False, default=None)

    @declared_attr
    def tunjangan_khusus_valid(cls):
        return Column(Date, nullable=False, default=None)

    @declared_attr
    def karyawan_valid(cls):
        return Column(Date, nullable=False, default=None)

    @declared_attr
    def lembur_valid(cls):
        return Column(Date, nullable=False, default=None)

    @declared_attr
    def absen_valid(cls):
        return Column(Date, nullable=False, default=None)

    @declared_attr
    def angsuran_valid(cls):
        return Column(Date, nullable=False, default=None)

    '''
    def mx_init(
        self,
        periode,
        pengubah_id=0,
        pengubah_name="Init",
        terakhir_diubah=None,
        job_level_valid=None,
        tunjangan_khusus_valid=None,
        karyawan_valid=None,
        lembur_valid=None,
        absen_valid=None,
        angsuran_valid=None
    ):
        terakhir_diubah = terakhir_diubah or date.today()
        self.periode = periode
        self.pengubah_id = pengubah_id
        self.pengubah_name = pengubah_name
        self.terakhir_diubah = terakhir_diubah
        self.job_level_valid = job_level_valid
        self.tunjangan_khusus_valid = tunjangan_khusus_valid
        self.karyawan_valid = karyawan_valid
        self.lembur_valid = lembur_valid
        self.absen_valid = absen_valid
        self.angsuran_valid = angsuran_valid
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "periode=%r, pengubah_id=%r, terakhir_diubah=%r, job_level_valid=%r, tunjangan_khusus_valid=%r, karyawan_valid=%r, lembur_valid=%r, absen_valid=%r, angsuran_valid=%r" % (self.periode, self.pengubah_id, self.terakhir_diubah, self.job_level_valid, self.tunjangan_khusus_valid, self.karyawan_valid, self.lembur_valid, self.absen_valid, self.angsuran_valid)

    def mx_init_repr(self):
        return {
            'periode': self.periode,
            'pengubah_id': self.pengubah_id,
            'pengubah_name': self.pengubah_name,
            'terakhir_diubah': self.terakhir_diubah,
            'job_level_valid': self.job_level_valid,
            'tunjangan_khusus_valid': self.tunjangan_khusus_valid,
            'karyawan_valid': self.karyawan_valid,
            'lembur_valid': self.lembur_valid,
            'absen_valid': self.absen_valid,
            'angsuran_valid': self.angsuran_valid
        }
