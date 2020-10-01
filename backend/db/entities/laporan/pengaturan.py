from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPengaturanBase, MxCommited


class DbPengaturan(MxCommited, MxPengaturanBase, DbLaporanEntity):
    pass
