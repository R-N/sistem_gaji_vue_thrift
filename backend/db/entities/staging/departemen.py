from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxDepartemen, MxStaging


class DbDepartemen(MxStaging, MxDepartemen, DbStagingEntity):
    pass
