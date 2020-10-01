from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbStagingEntity
from ..mixin import MxSubdepartemen, MxStaging
from .departemen import DbDepartemen


class DbSubdepartemen(MxStaging, MxSubdepartemen, DbStagingEntity):

    @hybrid_property
    def real_enabled(self):
        return self.enabled and self.departemen.real_enabled

    @real_enabled.expression
    def real_enabled(cls):
        return cls.enabled & DbDepartemen.real_enabled
