from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxJabatan, MxStaging
from .job_level import DbJobLevel


class DbJabatan(MxStaging, MxJabatan, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.enabled and self.job_level.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return cls.enabled & DbJobLevel.real_enabled
