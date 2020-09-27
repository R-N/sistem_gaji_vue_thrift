from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxAngsuran, MxStaging


class DbAngsuran(MxStaging, MxAngsuran, DbStagingEntity):
    pass
