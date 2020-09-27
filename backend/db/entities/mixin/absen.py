from sqlalchemy import Column, Integer, String, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode, insert_periode


class MxAbsen:
    __tablename__ = 'absen'

    @declared_attr
    def karyawan_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def tanggal(cls):
        return Column(Date, primary_key=True)
    # PK karyawan_id & tanggal
    @declared_attr
    def durasi(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def keterangan(cls):
        return Column(String(256), nullable=False)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="absen", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "karyawan_id"]),
                pop_periode(cls, ["karyawan.periode", "karyawan.no_induk"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        karyawan_id,
        tanggal,
        durasi,
        keterangan
    ):
        self.karyawan_id = karyawan_id
        self.tanggal = tanggal
        self.durasi = durasi
        self.keterangan = keterangan

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "karyawan_id=%r, tanggal=%r, durasi=%r" % (self.karyawan_id, self.tanggal, self.durasi)

    # this doesn't need declared_attr, does it?
    def get_potongan_persen(self, koef):
        return koef * (1 + self.durasi // 60)
