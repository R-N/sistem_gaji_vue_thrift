from sqlalchemy import Column, String, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxPengaturanBase:
    __tablename__ = 'pengaturan'

    # TODO: Set precision & scale for Numerics
    @declared_attr
    def perusahaan_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def mengetahui_nama(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def perusahaan(cls):
        return relationship("DbPerusahaan", back_populates="pengaturan", uselist=False, passive_deletes="all")

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "perusahaan_id"]),
                pop_periode(cls, ["perusahaan.periode", "perusahaan.id"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

    '''
    def mx_init(
        self,
        nama_mengetahui,
        perusahaan_id=1
    ):
        self.nama_mengetahui = nama_mengetahui
        self.perusahaan_id = perusahaan_id
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return ''

    '''
    def mx_repr(self):
        return "TODO" % (
            self.id, self.nama,
        )
    '''

    def mx_init_repr(self):
        return {
            'nama_mengetahui': self.nama_mengetahui,
            'perusahaan_id': self.perusahaan_id
        }
