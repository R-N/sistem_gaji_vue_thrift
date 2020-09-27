from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxLembur, MxStaging


class DbLembur(MxStaging, MxLembur, DbStagingEntity):
    pass
