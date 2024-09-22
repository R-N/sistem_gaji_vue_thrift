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
    def name(cls):
        return Column(String(perusahaan_constants.NAME_MAX_LEN), unique=True, nullable=False)

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
        name
    ):
        self.name = name
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_base_repr(self):
        return "id=%r, name=%r" % (self.id, self.name,)

    def mx_init_repr(self):
        return {
            'name': self.name,
            'id': self.id
        }

    # Properties and other methods associated with columns

    # name

    @validates("name")
    def validate_name(self, key, name):
        DbPerusahaanValidator.validate_name(name)
        return name

    # Other methods

    def fill(self, obj):
        obj.id = self.id
        obj.name = self.name
        obj.enabled = self.enabled

        return obj

    # validator

    def validator():
        return DbPerusahaanValidator

class DbPerusahaanValidator:
    pass

bind_rules(DbPerusahaanValidator, create_rules_fields(
    TPerusahaanError,
    ["NAME"],
    perusahaan_constants,
    {}, 
    TPerusahaanErrorCode, 
    T_PERUSAHAAN_ERROR_STR, 
    "PERUSAHAAN"
))

