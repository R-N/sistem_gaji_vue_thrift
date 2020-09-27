from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxStaging


class DbPerusahaan(MxStaging, MxPerusahaan, DbLaporanEntity):
    pass
