import re

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from .general import MxAiId

from rpc.gen.data.perusahaan.errors.ttypes import TPerusahaanError, TPerusahaanErrorCode
import rpc.gen.data.perusahaan.errors.constants as perusahaan_constants


class MxPerusahaan(MxAiId):
    __tablename__ = 'perusahaan'

    # Columns

    @declared_attr
    def _nama(cls):
        return Column("nama", String(perusahaan_constants.NAMA_LEN_MAX), unique=True, nullable=False)

    # Relationships

    @declared_attr
    def departemen(cls):
        return relationship("DbDepartemen", back_populates="perusahaan", viewonly=True)

    @declared_attr
    def pengaturan(cls):
        return relationship("DbPengaturan", back_populates="perusahaan", uselist=False)

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

    @declared_attr
    def nama(cls):
        @hybrid_property
        def nama(self):
            return self._nama

        @nama.setter
        def nama(self, nama):
            DbPerusahaanValidator.validate_nama(nama)
            self._nama = nama

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
    NAMA_REGEX = re.compile(perusahaan_constants.NAMA_REGEX_STR)

    def validate_nama(nama):
        if not nama:
            raise TPerusahaanError(TPerusahaanErrorCode.NAMA_EMPTY)
        if len(nama) > perusahaan_constants.NAMA_LEN_MAX:
            raise TPerusahaanError(TPerusahaanErrorCode.NAMA_TOO_LONG)
        if not DbPerusahaanValidator.NAMA_REGEX.match(nama):
            raise TPerusahaanError(TPerusahaanErrorCode.NAMA_INVALID)
