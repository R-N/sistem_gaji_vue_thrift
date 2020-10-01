from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxPeriodeGaji, MxStagingLite


class DbPeriodeGaji(MxStagingLite, MxPeriodeGaji, DbStagingEntity):
    pass
