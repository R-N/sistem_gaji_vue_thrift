from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxDepartemen, MxStaging
from .perusahaan import DbPerusahaan


class DbDepartemen(MxStaging, MxDepartemen, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.enabled and self.perusahaan.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return cls.enabled & DbPerusahaan.real_enabled
