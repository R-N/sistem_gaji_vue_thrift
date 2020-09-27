from sqlalchemy import Column, Integer, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode


class MxAngsuran(MxAiId):
    __tablename__ = 'angsuran'

    @declared_attr
    def karyawan_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def jenis_angsuran_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def tanggal(cls):
        return Column(Date, nullable=False)

    @declared_attr
    def total(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def _cicilan(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def terbayar(cls):
        return Column(Integer, nullable=False, default=0)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="angsuran", uselist=False)

    @declared_attr
    def jenis_angsuran(cls):
        return relationship("DbJenisAngsuran", back_populates="angsuran", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "karyawan_id"]),
                pop_periode(cls, ["karyawan.periode", "karyawan.no_induk"]),
                deferrable=True
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "jenis_angsuran_id"]),
                pop_periode(cls, ["jenis_angsuran.periode", "jenis_angsuran.id"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        karyawan_id,
        jenis_angsuran,
        tanggal,
        total,
        cicilan,
        terbayar=0
    ):
        self.karyawan_id = karyawan_id
        self.jenis_angsuran = jenis_angsuran
        self.tanggal = tanggal
        self.total = total
        self.cicilan = cicilan
        self.terbayar = terbayar

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, karyawan_id=%r, jenis_angsuran=%r, tanggal=%r, total=%r, cicilan=%r, terbayar=%r" % (self.id, self.karyawan_id, self.jenis_angsuran, self.tanggal, self.total, self.cicilan, self.terbayar)

    @declared_attr
    def sisa(cls):
        @hybrid_property
        def sisa(self):
            return max(self.total - self.terbayar, 0)
        return sisa

    @declared_attr
    def cicilan(cls):
        @hybrid_property
        def cicilan(self):
            return min(self._cicilan, self.sisa)

        @cicilan.setter
        def cicilan(self, value):
            if value > self.sisa:
                raise Exception("Cicilan tidak boleh lebih besar dari sisa")
            self._cicilan = value
        return cicilan

    @declared_attr
    def terbayar_akhir(cls):
        @hybrid_property
        def terbayar_akhir(self):
            return self.terbayar + self.cicilan
        return terbayar_akhir

    @declared_attr
    def sisa_akhir(cls):
        @hybrid_property
        def sisa_akhir(self):
            return self.sisa - self.cicilan
        return sisa_akhir
