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
    def _name(cls):
        return Column("name", String(50), unique=True, nullable=False)

    @declared_attr
    def jabatan(cls):
        return relationship("DbJabatan", back_populates="job_level", viewonly=True, passive_deletes="all")

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

    def mx_repr(self):
        return "id=%r, name=%r" % (self.id, self.name)

    def mx_init_repr(self):
        return {
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
            DbJobLevelBaseValidator.validate_name(name)
            self._name = name

        return name

    # Other methods

    def fill_base(self, obj):
        obj.id = self.id
        obj.name = self.name
        obj.enabled = self.enabled

        return obj
    
    def fill(self, obj):
        return self.fill_base(obj)

    # validator

    def validator():
        return DbJobLevelBaseValidator

class DbJobLevelBaseValidator:
    NAME_REGEX = re.compile(job_level_constants.NAME_REGEX_STR)

    def validate_name(name):
        if not name:
            raise TJobLevelError(TJobLevelErrorCode.NAME_EMPTY)
        if len(name) > job_level_constants.NAME_MAX_LEN:
            raise TJobLevelError(TJobLevelErrorCode.NAME_TOO_LONG)
        if not DbJobLevelBaseValidator.NAME_REGEX.match(name):
            raise TJobLevelError(TJobLevelErrorCode.NAME_INVALID)
