from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxMasaKerja, MxCommited


class DbMasaKerja(MxCommited, MxMasaKerja, DbCommitedEntity):
    pass
