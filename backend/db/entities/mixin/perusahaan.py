import re

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from .general import MxAiId

from rpc.gen.data.perusahaan.errors.ttypes import TPerusahaanError, TPerusahaanErrorCode
import rpc.gen.data.perusahaan.errors.constants as perusahaan_constants
from rpc.gen.data.perusahaan.errors.constants import T_PERUSAHAAN_ERROR_STR
from ...validator import bind_rules, create_rules_fields


class MxPerusahaan(MxAiId):
    __tablename__ = 'perusahaan'

    # Columns

    @declared_attr
    def nama(cls):
        return Column(String(perusahaan_constants.NAMA_MAX_LEN), unique=True, nullable=False)

    # Relationships

    @declared_attr
    def departemen(cls):
        return relationship("DbDepartemen", back_populates="perusahaan", viewonly=True, passive_deletes="all")

    @declared_attr
    def pengaturan(cls):
        return relationship("DbPengaturan", back_populates="perusahaan", uselist=False, passive_deletes="all")

    # Inits and stuff

    '''
    def mx_init(
        self,
        id,
        nama
    ):
        self.nama = nama
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_base_repr(self):
        return "id=%r, nama=%r" % (self.id, self.nama,)

    def mx_init_repr(self):
        return {
            'nama': self.nama,
            'id': self.id
        }

    # Properties and other methods associated with columns

    # nama

    @validates("nama")
    def validate_nama(self, key, nama):
        DbPerusahaanValidator.validate_nama(nama)
        return nama

    # Other methods

    def fill(self, obj):
        obj.id = self.id
        obj.nama = self.nama
        obj.enabled = self.enabled

        return obj

    # validator

    def validator():
        return DbPerusahaanValidator

class DbPerusahaanValidator:
    pass

bind_rules(DbPerusahaanValidator, create_rules_fields(
    TPerusahaanError,
    ["NAMA"],
    perusahaan_constants,
    {}, 
    TPerusahaanErrorCode, 
    T_PERUSAHAAN_ERROR_STR, 
    "PERUSAHAAN"
))

