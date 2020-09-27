from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxJobLevel, MxCommited


class DbJobLevel(MxCommited, MxJobLevel, DbCommitedEntity):
    pass
