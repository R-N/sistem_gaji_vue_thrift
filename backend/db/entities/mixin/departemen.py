from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode, eager_load_staging_parent
from sqlalchemy.ext.hybrid import hybrid_property

from rpc.gen.data.departemen.errors.ttypes import TDepartemenError, TDepartemenErrorCode
import rpc.gen.data.departemen.errors.constants as departemen_constants
import re


class MxDepartemen(MxAiId):
    __tablename__ = 'departemen'

    @declared_attr
    def _nama(cls):
        return Column("nama", String(50), nullable=False)

    @declared_attr
    def perusahaan_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def perusahaan(cls):
        return relationship(
            "DbPerusahaan",
            back_populates="departemen",
            uselist=False,
            lazy=eager_load_staging_parent(cls)
        )

    @declared_attr
    def subdepartemen(cls):
        return relationship("DbSubdepartemen", back_populates="departemen", viewonly=True, passive_deletes="all")

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "perusahaan_id"]),
                pop_periode(cls, ["perusahaan.periode", "perusahaan.id"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

        '''
    def mx_init(
        self,
        id,
        perusahaan_id,
        nama
    ):
        self.perusahaan_id = perusahaan_id
        self.nama = nama
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, perusahaan_id=%r, nama=%r" % (self.id, self.perusahaan_id, self.nama)

    def mx_init_repr(self):
        return {
            'perusahaan_id': self.perusahaan_id,
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
            DbDepartemenValidator.validate_nama(nama)
            self._nama = nama

        return nama

    # Other methods

    def fill(self, obj):
        obj.id = self.id
        obj.nama = self.nama
        obj.enabled = self.enabled
        obj.perusahaan_id = self.perusahaan_id

        return obj

    # validator

    def validator():
        return DbDepartemenValidator


class DbDepartemenValidator:
    NAMA_REGEX = re.compile(departemen_constants.NAMA_REGEX_STR)

    def validate_nama(nama):
        if not nama:
            raise TDepartemenError(TDepartemenErrorCode.NAMA_EMPTY)
        if len(nama) > departemen_constants.NAMA_MAX_LEN:
            raise TDepartemenError(TDepartemenErrorCode.NAMA_TOO_LONG)
        if not DbDepartemenValidator.NAMA_REGEX.match(nama):
            raise TDepartemenError(TDepartemenErrorCode.NAMA_INVALID)
