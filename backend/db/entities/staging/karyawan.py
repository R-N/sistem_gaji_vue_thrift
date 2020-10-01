from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxKaryawan, MxStaging
from .jabatan import DbJabatan
from .subdepartemen import DbSubdepartemen


class DbKaryawan(MxStaging, MxKaryawan, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.enabled and self.jabatan.real_enabled and self.subdepartemen.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return cls.enabled & DbJabatan.real_enabled & DbSubdepartemen.real_enabled
