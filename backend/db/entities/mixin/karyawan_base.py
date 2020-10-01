from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxKaryawanBase:
    __tablename__ = 'karyawan'

    @declared_attr
    def no_induk(cls):
        return Column(Integer, primary_key=True, nullable=False)

    @declared_attr
    def nama(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def email(cls):
        return Column(String(50), nullable=False)

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
        )

    '''
    def mx_init(
        self,
        no_induk,
        nama,
        email,
        subdepartemen_id,
        jabatan_id
    ):
        self.no_induk = no_induk
        self.nama = nama
        self.email = email
        self.subdepartemen_id = subdepartemen_id
        self.jabatan_id = jabatan_id
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "no_induk=%r, nama=%r, subdepartemen_id=%r, jabatan_id=%r" % (self.no_induk, self.nama, self.subdepartemen_id, self.jabatan_id)

    def mx_init_repr(self):
        return {
            'no_induk': self.no_induk,
            'nama': self.nama,
            'email': self.email,
            'subdepartemen_id': self.subdepartemen_id,
            'jabatan_id': self.jabatan_id
        }