from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxJabatan, MxStaging


class DbJabatan(MxStaging, MxJabatan, DbStagingEntity):
    pass
