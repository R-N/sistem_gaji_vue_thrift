from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode
from .secondary import ScTunjanganKhususJabatan


class MxJabatan(MxAiId):
    __tablename__ = 'jabatan'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def job_level_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def job_level(cls):
        return relationship("DbJobLevel", back_populates="jabatan", uselist=False)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="jabatan", viewonly=True)

    @declared_attr
    def ScTunjanganKhususJabatan(cls):
        return ScTunjanganKhususJabatan(cls.metadata, cls)

    @declared_attr
    def tunjangan_khusus(cls):
        return relationship("DbTunjanganKhusus", back_populates="jabatan", secondary=lambda: cls.ScTunjanganKhususJabatan)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "job_level_id"]),
                pop_periode(cls, ["job_level.periode", "job_level.id"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        job_level_id,
        nama
    ):
        self.nama = nama
        self.job_level_id = job_level_id

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, job_level_id=%r, nama=%r" % (self.id, self.job_level_id, self.nama)
