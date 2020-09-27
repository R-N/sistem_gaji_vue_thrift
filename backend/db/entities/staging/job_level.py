from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxJobLevel, MxStaging


class DbJobLevel(MxStaging, MxJobLevel, DbStagingEntity):
    pass
