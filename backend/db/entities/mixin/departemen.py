from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode, eager_load_staging_parent


class MxDepartemen(MxAiId):
    __tablename__ = 'departemen'

    @declared_attr
    def nama(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def perusahaan_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def perusahaan(cls):
        return relationship(
            "DbPerusahaan",
            back_populates="departemen",
            uselist=False,
            lazy=eager_load_staging_parent(cls)
        )

    @declared_attr
    def subdepartemen(cls):
        return relationship("DbSubdepartemen", back_populates="departemen", viewonly=True)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "perusahaan_id"]),
                pop_periode(cls, ["perusahaan.periode", "perusahaan.id"]),
                deferrable=True
            ),
        )

        '''
    def mx_init(
        self,
        id,
        perusahaan_id,
        nama
    ):
        self.perusahaan_id = perusahaan_id
        self.nama = nama
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, perusahaan_id=%r, nama=%r" % (self.id, self.perusahaan_id, self.nama)

    def mx_init_repr(self):
        return {
            'perusahaan_id': self.perusahaan_id,
            'nama': self.nama,
            'id': self.id
        }
