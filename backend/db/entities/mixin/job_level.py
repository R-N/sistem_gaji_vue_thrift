from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId


class MxJobLevel(MxAiId):
    __tablename__ = 'job_level'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def gaji_pokok(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def tunjangan_jabatan(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def upah_lembur_1(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def upah_lembur_2(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def upah_lembur_3(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def tunjangan_kinerja(cls):
        return relationship("DbTunjanganKinerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganKinerja.kinerja")

    @declared_attr
    def tunjangan_masa_kerja(cls):
        return relationship("DbTunjanganMasaKerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganMasaKerja.batas_bawah")

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="job_level", viewonly=True)

    def mx_init(
        self,
        nama,
        gaji_pokok,
        tunjangan_jabatan
    ):
        self.nama = nama
        self.gaji_pokok = gaji_pokok
        self.tunjangan_jabatan = tunjangan_jabatan

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, nama=%r, gaji_pokok=%r, tunjangan_jabatan=%r" % (self.id, self.nama, self.gaji_pokok, self.tunjangan_jabatan)

    @declared_attr
    def upah_lembur(cls):
        @hybrid_property
        def upah_lembur(self):
            return [self.upah_lembur_1, self.upah_lembur_2, self.upah_lembur_3]
        return upah_lembur
