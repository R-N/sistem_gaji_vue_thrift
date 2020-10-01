from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxPeriodeGaji, MxRepr


class DbPeriodeGaji(MxRepr, MxPeriodeGaji, DbCommitedEntity):
    pass
