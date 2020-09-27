from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxAbsen, MxStaging


class DbAbsen(MxStaging, MxAbsen, DbStagingEntity):
    pass
