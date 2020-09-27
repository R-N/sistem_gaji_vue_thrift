from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxLembur, MxCommited


class DbLembur(MxCommited, MxLembur, DbCommitedEntity):
    pass
