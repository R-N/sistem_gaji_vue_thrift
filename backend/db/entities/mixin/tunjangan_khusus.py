from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId
from .secondary import ScTunjanganKhususJabatan


class MxTunjanganKhusus(MxAiId):
    __tablename__ = 'tunjangan_khusus'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def nilai(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="tunjangan_khusus", secondary=lambda: cls.ScTunjanganKhususJabatan)

    @declared_attr
    def ScTunjanganKhususJabatan(cls):
        return ScTunjanganKhususJabatan(cls.metadata, cls)

    '''
    def mx_init(
        self,
        id,
        nama,
        nilai
    ):
        self.nama = nama
        self.nilai = nilai
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, nama=%r, nilai=%r" % (self.id, self.nama, self.nilai)

    def mx_init_repr(self):
        return {
            'nama': self.nama,
            'nilai': self.nilai,
            'id': self.id
        }
