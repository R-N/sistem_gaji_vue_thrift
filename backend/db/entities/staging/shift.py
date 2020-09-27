from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxShift, MxStaging


class DbShift(MxStaging, MxShift, DbStagingEntity):
    pass
