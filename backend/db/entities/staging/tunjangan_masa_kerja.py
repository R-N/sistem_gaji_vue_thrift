from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxTunjanganMasaKerja, MxStagingLite
from .job_level import DbJobLevel


class DbTunjanganMasaKerja(MxStagingLite, MxTunjanganMasaKerja, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.job_level.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return DbJobLevel.real_enabled
