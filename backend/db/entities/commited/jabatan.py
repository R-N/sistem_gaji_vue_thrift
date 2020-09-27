from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxJabatan, MxCommited


class DbJabatan(MxCommited, MxJabatan, DbCommitedEntity):
    pass
