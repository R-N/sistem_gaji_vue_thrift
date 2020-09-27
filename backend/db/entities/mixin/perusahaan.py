from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId


class MxPerusahaan(MxAiId):
    __tablename__ = 'perusahaan'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def departemen(cls):
        return relationship("DbDepartemen", back_populates="perusahaan", viewonly=True)

    @declared_attr
    def pengaturan(cls):
        return relationship("DbPengaturan", back_populates="perusahaan", uselist=False)

    def mx_init(
        self,
        nama
    ):
        self.nama = nama

    def mx_reconstruct(self):
        pass

    def mx_base_repr(self):
        return "id=%r, nama=%r" % (self.id, self.nama,)
