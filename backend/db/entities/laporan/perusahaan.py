from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxCommited


class DbPerusahaan(MxCommited, MxPerusahaan, DbLaporanEntity):
    pass
