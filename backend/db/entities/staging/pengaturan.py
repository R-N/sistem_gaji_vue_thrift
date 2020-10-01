from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxPengaturan, MxStagingLite


class DbPengaturan(MxStagingLite, MxPengaturan, DbStagingEntity):
    pass
