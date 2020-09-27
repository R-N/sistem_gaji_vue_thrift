from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxPeriodeGaji, MxCommited


class DbPeriodeGaji(MxCommited, MxPeriodeGaji, DbCommitedEntity):
    pass
