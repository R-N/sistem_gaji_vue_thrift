from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxMasaKerja, MxStaging


class DbMasaKerja(MxStaging, MxMasaKerja, DbStagingEntity):
    pass
