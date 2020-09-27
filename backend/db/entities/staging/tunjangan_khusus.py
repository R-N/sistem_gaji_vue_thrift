from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxTunjanganKhusus, MxStaging


class DbTunjanganKhusus(MxStaging, MxTunjanganKhusus, DbStagingEntity):
    pass
