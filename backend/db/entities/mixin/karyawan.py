from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode
from .karyawan_base import MxKaryawanBase
from utils.util import get_cls_attr


class MxKaryawan(MxKaryawanBase):

    @declared_attr
    def nik(cls):
        return Column(String(32), unique=True, nullable=False)

    @declared_attr
    def tanggal_masuk(cls):
        return Column(Date, nullable=False)

    @declared_attr
    def status(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def alamat(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def tempat_lahir(cls):
        return Column(String(50), nullable=True)

    @declared_attr
    def tanggal_lahir(cls):
        return Column(Date, nullable=True)

    @declared_attr
    def agama(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def jenis_kelamin(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def pendidikan(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def gaji_dilaporkan(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def perumahan(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def koperasi(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def kinerja(cls):
        return Column(String(1), nullable=True, default=None)

    @declared_attr
    def pph_21(cls):
        return Column(Integer, nullable=True, default=None)

    @declared_attr
    def thr(cls):
        return Column(Integer, nullable=False, default=0)

    @declared_attr
    def lain_lain(cls):
        return Column(Integer, nullable=False, default=0)
 
    @declared_attr
    def kinerja_rel(cls):
        return relationship("DbKinerja", back_populates="karyawan", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return get_cls_attr(MxKaryawanBase, '__table_args__').fget(cls) + (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "kinerja"]),
                pop_periode(cls, ["kinerja.periode", "kinerja.kode"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

    '''
    def mx_init(
        self,
        *args,
        nik,
        status,
        alamat,
        tanggal_masuk=None,
        tempat_lahir=None,
        tanggal_lahir=None,
        agama=None,
        jenis_kelamin=None,
        pendidikan=None,
        gaji_dilaporkan=None,
        perumahan=False,
        koperasi=False,
        kinerja=None,
        pph_21=None,
        lain_lain=0,
        **kwargs
    ):
        MxKaryawanBase.mx_init(self, *args, **kwargs)
        tanggal_masuk = tanggal_masuk or date.today()
        self.nik = nik
        self.status = status
        self.alamat = alamat
        self.tanggal_masuk = tanggal_masuk
        self.tempat_lahir = tempat_lahir
        self.tanggal_lahir = tanggal_lahir
        self.agama = agama
        self.jenis_kelamin = jenis_kelamin
        self.pendidikan = pendidikan
        self.gaji_dilaporkan = gaji_dilaporkan
        self.perumahan = perumahan
        self.koperasi = koperasi
        self.kinerja = kinerja
        self.pph_21 = pph_21
        self.lain_lain = lain_lain
    '''

    def mx_reconstruct(self):
        MxKaryawanBase.mx_reconstruct(self)

    def mx_repr(self):
        return "%s" % (MxKaryawanBase.mx_repr(self),)

    def mx_init_repr(self):
        ret = MxKaryawanBase.mx_init_repr(self)
        ret.update({
            'nik': self.nik,
            'status': self.status,
            'alamat': self.alamat,
            'tanggal_masuk': self.tanggal_masuk,
            'tempat_lahir': self.tempat_lahir,
            'tanggal_lahir': self.tanggal_lahir,
            'agama': self.agama,
            'jenis_kelamin': self.jenis_kelamin,
            'pendidikan': self.pendidikan,
            'gaji_dilaporkan': self.gaji_dilaporkan,
            'perumahan': self.perumahan,
            'koperasi': self.koperasi,
            'kinerja': self.kinerja,
            'pph_21': self.pph_21,
            'lain_lain': self.lain_lain
        })
        return ret
