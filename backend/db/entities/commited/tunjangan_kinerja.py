from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxTunjanganKinerja, MxCommited


class DbTunjanganKinerja(MxCommited, MxTunjanganKinerja, DbCommitedEntity):
    pass
