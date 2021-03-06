from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxAngsuran, MxCommited


class DbAngsuran(MxCommited, MxAngsuran, DbCommitedEntity):
    pass
