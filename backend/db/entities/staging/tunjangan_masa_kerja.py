from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxTunjanganMasaKerja, MxStaging


class DbTunjanganMasaKerja(MxStaging, MxTunjanganMasaKerja, DbStagingEntity):
    pass
