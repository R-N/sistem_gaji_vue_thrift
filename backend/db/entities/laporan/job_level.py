from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxJobLevelBase, MxCommited


class DbJobLevel(MxCommited, MxJobLevelBase, DbLaporanEntity):
    pass
