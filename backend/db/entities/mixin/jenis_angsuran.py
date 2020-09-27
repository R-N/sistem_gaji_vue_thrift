from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId

class MxJenisAngsuran(MxAiId):
    __tablename__ = 'jenis_angsuran'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def jenis(cls):
        return Column(Integer, nullable=False, default=1)

    @declared_attr
    def angsuran(cls):
        return relationship("DbAngsuran", back_populates="jenis_angsuran", viewonly=True)

    def mx_init(
        self,
        nama,
        jenis=1
    ):
        self.nama = nama
        self.jenis = jenis

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, nama=%r, jenis=%r" % (self.id, self.nama, self.jenis)
