from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class MxKinerja:
    __tablename__ = 'kinerja'

    @declared_attr
    def kode(cls):
        return Column(String(1), primary_key=True, nullable=False)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="kinerja_rel", viewonly=True)

    def mx_init(
        self,
        kode
    ):
        self.kode = kode

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "kode=%r" % (self.kode,)
