from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxKaryawan:
    __tablename__ = 'karyawan'

    @declared_attr
    def no_induk(cls):
        return Column(Integer, primary_key=True, nullable=False)

    @declared_attr
    def nik(cls):
        return Column(String(32), unique=True, nullable=False)

    @declared_attr
    def nama(cls):
        return Column(String(50), nullable=False)

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
    def email(cls):
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
        return Column(String(1), nullable=True)

    @declared_attr
    def thr(cls):
        return Column(Integer, nullable=False, default=0)

    @declared_attr
    def lain_lain(cls):
        return Column(Integer, nullable=False, default=0)
 
    @declared_attr
    def subdepartemen_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def subdepartemen(cls):
        return relationship("DbSubdepartemen", back_populates="karyawan", uselist=False)

    @declared_attr
    def jabatan_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="karyawan", uselist=False)

    @declared_attr
    def angsuran(cls):
        return relationship("DbAngsuran", back_populates="karyawan", viewonly=True)

    @declared_attr
    def lembur(cls):
        return relationship("DbLembur", back_populates="karyawan", viewonly=True)

    @declared_attr
    def absen(cls):
        return relationship("DbAbsen", back_populates="karyawan", viewonly=True)

    @declared_attr
    def kinerja_rel(cls):
        return relationship("DbKinerja", back_populates="karyawan", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "subdepartemen_id"]),
                pop_periode(cls, ["subdepartemen.periode", "subdepartemen.id"]),
                deferrable=True
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "jabatan_id"]),
                pop_periode(cls, ["jabatan.periode", "jabatan.id"]),
                deferrable=True
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "kinerja"]),
                pop_periode(cls, ["kinerja.periode", "kinerja.kode"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        no_induk,
        nik,
        nama,
        status,
        alamat,
        email,
        subdepartemen_id,
        jabatan_id,
        enabled=True,
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
        lain_lain=0
    ):
        tanggal_masuk = tanggal_masuk or date.today()
        self.no_induk = no_induk
        self.nik = nik
        self.nama = nama
        self.status = status
        self.alamat = alamat
        self.email = email
        self.subdepartemen_id = subdepartemen_id
        self.jabatan_id = jabatan_id
        self.enabled = enabled
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
        self.lain_lain = lain_lain

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "no_induk=%r, nama=%r, subdepartemen_id=%r, jabatan=%r" % (self.no_induk, self.nama, self.subdepartemen_id, self.jabatan_id)
