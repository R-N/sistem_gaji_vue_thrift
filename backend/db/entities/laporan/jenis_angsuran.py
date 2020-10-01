from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxJenisAngsuran, MxCommited


class DbJenisAngsuran(MxCommited, MxJenisAngsuran, DbLaporanEntity):
    pass
