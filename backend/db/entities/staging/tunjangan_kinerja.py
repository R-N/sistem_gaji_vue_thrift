from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxTunjanganKinerja, MxStaging


class DbTunjanganKinerja(MxStaging, MxTunjanganKinerja, DbStagingEntity):
    pass
