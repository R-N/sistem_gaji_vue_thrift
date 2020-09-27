from sqlalchemy import Column, String, Integer, Numeric, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxPengaturan:
    __tablename__ = 'pengaturan'

    # TODO: Set precision & scale for Numerics
    @declared_attr
    def perusahaan_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def bpjs_ketenagakerjaan_perusahaan(cls):
        return Column(Numeric, nullable=False)

    @declared_attr
    def bpjs_ketenagakerjaan_karyawan(cls):
        return Column(Numeric, nullable=False)

    @declared_attr
    def bpjs_kesehatan_perusahaan(cls):
        return Column(Numeric, nullable=False)

    @declared_attr
    def bpjs_kesehatan_karyawan(cls):
        return Column(Numeric, nullable=False)

    @declared_attr
    def upah_minimum(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def iuran_rumah(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def iuran_koperasi(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def pendaftaran_koperasi(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def uang_makan(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def uang_transport(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def nama_mengetahui(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def perusahaan(cls):
        return relationship("DbPerusahaan", back_populates="pengaturan", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "perusahaan_id"]),
                pop_periode(cls, ["perusahaan.periode", "perusahaan.id"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        bpjs_ketenagakerjaan_perusahaan,
        bpjs_ketenagakerjaan_karyawan,
        bpjs_kesehatan_perusahaan,
        bpjs_kesehatan_karyawan,
        upah_minimum,
        iuran_rumah,
        iuran_koperasi,
        pendaftaran_koperasi,
        uang_makan,
        uang_transport,
        nama_mengetahui,
        perusahaan_id=1
    ):
        self.bpjs_ketenagakerjaan_perusahaan = bpjs_ketenagakerjaan_perusahaan
        self.bpjs_ketenagakerjaan_karyawan = bpjs_ketenagakerjaan_karyawan
        self.bpjs_kesehatan_perusahaan = bpjs_kesehatan_perusahaan
        self.bpjs_ketenagakerjaan_karyawan = bpjs_ketenagakerjaan_karyawan
        self.upah_minimum = upah_minimum
        self.iuran_rumah = iuran_rumah
        self.iuran_koperasi = iuran_koperasi
        self.pendaftaran_koperasi = pendaftaran_koperasi
        self.uang_makan = uang_makan
        self.uang_transport = uang_transport
        self.nama_mengetahui = nama_mengetahui
        self.perusahaan_id = perusahaan_id

    def mx_reconstruct(self):
        pass

    def mx_base_repr(self):
        return ''

    '''
    def mx_base_repr(self):
        return "TODO" % (
            self.id, self.nama,
        )
    '''