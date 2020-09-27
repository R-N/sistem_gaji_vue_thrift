from sqlalchemy import Column, Date
from sqlalchemy.ext.declarative import declared_attr


class MxPeriodeGaji:
    __tablename__ = 'periode_gaji'

    @declared_attr
    def periode(cls):
        return Column(Date, primary_key=True)

    @declared_attr
    def terakhir_direvisi(cls):
        return Column(Date, nullable=True, default=None)

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

    def mx_init(
        self,
        periode,
        terakhir_direvisi=None,
        job_level_valid=None,
        tunjangan_khusus_valid=None,
        karyawan_valid=None,
        lembur_valid=None,
        absen_valid=None,
        angsuran_valid=None
    ):
        self.periode = periode
        self.terakhir_direvisi = terakhir_direvisi
        self.job_level_valid = job_level_valid
        self.tunjangan_khusus_valid = tunjangan_khusus_valid
        self.karyawan_valid = karyawan_valid
        self.lembur_valid = lembur_valid
        self.absen_valid = absen_valid
        self.angsuran_valid = angsuran_valid

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "periode=%r, terakhir_direvisi=%r, job_level_valid=%r, tunjangan_khusus_valid=%r, karyawan_valid=%r, lembur_valid=%r, absen_valid=%r, angsuran_valid=%r" % (self.periode, self.terakhir_direvisi, self.job_level_valid, self.tunjangan_khusus_valid, self.karyawan_valid, self.lembur_valid, self.absen_valid, self.angsuran_valid)
