from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.ext.declarative import declared_attr
from .pengaturan_base import MxPengaturanBase


class MxPengaturan(MxPengaturanBase):
    # TODO: Set precision & scale for Numerics
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
    def koef_absen(cls):
        return Column(Numeric, nullable=False)

    '''
    def mx_init(
        self,
        *args,
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
        koef_absen,
        **kwargs
    ):
        MxPengaturanBase.mx_init(*args, **kwargs)
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
        self.koef_absen = koef_absen
    '''

    def mx_reconstruct(self):
        MxPengaturanBase.mx_reconstruct(self)

    def mx_repr(self):
        return '%s' % (MxPengaturanBase.mx_repr(self),)

    '''
    def mx_repr(self):
        return "TODO" % (
            self.id, self.nama,
        )
    '''

    def mx_init_repr(self):
        ret = MxPengaturanBase.mx_init_repr(self)
        ret.update({
            'bpjs_ketenagakerjaan_perusahaan': self.bpjs_ketenagakerjaan_perusahaan,
            'bpjs_ketenagakerjaan_karyawan': self.bpjs_ketenagakerjaan_karyawan,
            'bpjs_kesehatan_perusahaan': self.bpjs_kesehatan_perusahaan,
            'bpjs_kesehatan_karyawan': self.bpjs_kesehatan_karyawan,
            'upah_minimum': self.upah_minimum,
            'iuran_rumah': self.iuran_rumah,
            'iuran_koperasi': self.iuran_koperasi,
            'pendaftaran_koperasi': self.pendaftaran_koperasi,
            'uang_makan': self.uang_makan,
            'uang_transport': self.uang_transport,
            'koef_absen': self.koef_absen
        })
        return ret
