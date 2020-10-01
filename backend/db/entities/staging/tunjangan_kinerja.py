from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxTunjanganKinerja, MxStagingLite
from .job_level import DbJobLevel
from .kinerja import DbKinerja


class DbTunjanganKinerja(MxStagingLite, MxTunjanganKinerja, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.job_level.real_enabled and self.kinerja_rel.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return DbJobLevel.real_enabled & DbKinerja.real_enabled
