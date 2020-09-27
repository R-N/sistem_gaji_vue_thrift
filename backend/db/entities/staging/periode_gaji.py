from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxPeriodeGaji, MxStaging


class DbPeriodeGaji(MxStaging, MxPeriodeGaji, DbStagingEntity):
    pass
