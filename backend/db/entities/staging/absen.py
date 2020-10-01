from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxAbsen, MxStaging
from .karyawan import DbKaryawan


class DbAbsen(MxStaging, MxAbsen, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.enabled and self.karyawan.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return cls.enabled & DbKaryawan.real_enabled
