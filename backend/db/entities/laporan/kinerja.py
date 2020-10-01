from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxKinerja, MxCommited


class DbKinerja(MxCommited, MxKinerja, DbLaporanEntity):
    pass
