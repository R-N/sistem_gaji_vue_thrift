from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxPengaturan, MxStaging


class DbPengaturan(MxStaging, MxPengaturan, DbStagingEntity):
    pass
