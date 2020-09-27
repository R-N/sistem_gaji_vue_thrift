from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxShift, MxCommited


class DbShift(MxCommited, MxShift, DbCommitedEntity):
    pass
