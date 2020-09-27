from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxPerusahaan, MxStaging


class DbPerusahaan(MxStaging, MxPerusahaan, DbStagingEntity):
    pass
