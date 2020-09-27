from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxTunjanganKhusus, MxCommited


class DbTunjanganKhusus(MxCommited, MxTunjanganKhusus, DbCommitedEntity):
    pass
