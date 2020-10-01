from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId


class MxJobLevelBase(MxAiId):
    __tablename__ = 'job_level'

    @declared_attr
    def nama(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="job_level", viewonly=True)

    '''
    def mx_init(
        self,
        id,
        nama
    ):
        self.nama = nama
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, nama=%r" % (self.id, self.nama)

    def mx_init_repr(self):
        return {
            'nama': self.nama,
            'id': self.id
        }
