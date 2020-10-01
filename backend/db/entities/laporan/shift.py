from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxShiftBase, MxCommited


class DbShift(MxCommited, MxShiftBase, DbLaporanEntity):
    pass
