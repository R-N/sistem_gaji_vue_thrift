from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxPengaturan, MxCommited


class DbPengaturan(MxCommited, MxPengaturan, DbCommitedEntity):
    pass
