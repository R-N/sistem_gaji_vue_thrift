from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId

class MxJenisAngsuran(MxAiId):
    __tablename__ = 'jenis_angsuran'

    @declared_attr
    def name(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def jenis(cls):
        return Column(Integer, nullable=False, default=1)

    @declared_attr
    def angsuran(cls):
        return relationship("DbAngsuran", back_populates="jenis_angsuran", viewonly=True, passive_deletes="all")

        '''
    def mx_init(
        self,
        id,
        name,
        jenis=1
    ):
        self.name = name
        self.jenis = jenis
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, name=%r, jenis=%r" % (self.id, self.name, self.jenis)

    def mx_init_repr(self):
        return {
            'name': self.name,
            'jenis': self.jenis,
            'id': self.id
        }
