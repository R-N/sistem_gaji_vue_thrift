from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxTunjanganMasaKerja, MxCommited


class DbTunjanganMasaKerja(MxCommited, MxTunjanganMasaKerja, DbCommitedEntity):
    pass
