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
    def _name(cls):
        return Column("name", String(50), nullable=False)

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
        name
    ):
        self.perusahaan_id = perusahaan_id
        self.name = name
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, perusahaan_id=%r, name=%r" % (self.id, self.perusahaan_id, self.name)

    def mx_init_repr(self):
        return {
            'perusahaan_id': self.perusahaan_id,
            'name': self.name,
            'id': self.id
        }

    # Properties and other methods associated with columns

    # name

    @declared_attr
    def name(cls):
        @hybrid_property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            DbDepartemenValidator.validate_name(name)
            self._name = name

        return name

    # Other methods

    def fill(self, obj):
        obj.id = self.id
        obj.name = self.name
        obj.enabled = self.enabled
        obj.perusahaan_id = self.perusahaan_id

        return obj

    # validator

    def validator():
        return DbDepartemenValidator


class DbDepartemenValidator:
    NAME_REGEX = re.compile(departemen_constants.NAME_REGEX_STR)

    def validate_name(name):
        if not name:
            raise TDepartemenError(TDepartemenErrorCode.NAME_EMPTY)
        if len(name) > departemen_constants.NAME_MAX_LEN:
            raise TDepartemenError(TDepartemenErrorCode.NAME_TOO_LONG)
        if not DbDepartemenValidator.NAME_REGEX.match(name):
            raise TDepartemenError(TDepartemenErrorCode.NAME_INVALID)
