from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxLembur:
    __tablename__ = 'lembur'

    @declared_attr
    def karyawan_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def tanggal(cls):
        return Column(Date, primary_key=True)
    # PK karyawan_id & tanggal
    @declared_attr
    def shift(cls):
        return Column(String(6), nullable=False)

    @declared_attr
    def durasi(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def keterangan(cls):
        return Column(String(256), nullable=False)

    @declared_attr
    def makan(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def transport(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="lembur", uselist=False)

    @declared_attr
    def shift_rel(cls):
        return relationship("DbShift", back_populates="lembur", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "karyawan_id"]),
                pop_periode(cls, ["karyawan.periode", "karyawan.no_induk"]),
                deferrable=True
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "shift"]),
                pop_periode(cls, ["shift.periode", "shift.kode"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        karyawan_id,
        tanggal,
        shift,
        durasi,
        keterangan,
        makan=False,
        transport=False
    ):
        self.karyawan_id = karyawan_id
        self.tanggal = tanggal
        self.shift = shift
        self.durasi = durasi
        self.keterangan = keterangan
        self.makan = makan
        self.transport = transport

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "karyawan_id=%r, tanggal=%r, shift=%r, durasi=%r, makan=%r, transport=%r" % (self.karyawan_id, self.tanggal, self.shift, self.durasi, self.makan, self.transport)
