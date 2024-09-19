from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from rpc.gen.data.job_level.errors.ttypes import TJobLevelError, TJobLevelErrorCode
import rpc.gen.data.job_level.errors.constants as job_level_constants
from .general import MxAiId
import re


class MxJobLevelBase(MxAiId):
    __tablename__ = 'job_level'

    @declared_attr
    def _nama(cls):
        return Column("nama", String(50), unique=True, nullable=False)

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="job_level", viewonly=True)

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

    def mx_repr(self):
        return "id=%r, nama=%r" % (self.id, self.nama)

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
            DbJobLevelBaseValidator.validate_nama(nama)
            self._nama = nama

        return nama

    # Other methods

    def fill_base(self, obj):
        obj.id = self.id
        obj.nama = self.nama
        obj.enabled = self.enabled

        return obj
    
    def fill(self, obj):
        return self.fill_base(obj)

    # validator

    def validator():
        return DbJobLevelBaseValidator

class DbJobLevelBaseValidator:
    NAMA_REGEX = re.compile(job_level_constants.NAMA_REGEX_STR)

    def validate_nama(nama):
        if not nama:
            raise TJobLevelError(TJobLevelErrorCode.NAMA_EMPTY)
        if len(nama) > job_level_constants.NAMA_LEN_MAX:
            raise TJobLevelError(TJobLevelErrorCode.NAMA_TOO_LONG)
        if not DbJobLevelBaseValidator.NAMA_REGEX.match(nama):
            raise TJobLevelError(TJobLevelErrorCode.NAMA_INVALID)
