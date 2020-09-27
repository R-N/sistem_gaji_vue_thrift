from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxAbsen, MxCommited


class DbAbsen(MxCommited, MxAbsen, DbCommitedEntity):
    pass
