from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxKinerja, MxCommited


class DbKinerja(MxCommited, MxKinerja, DbCommitedEntity):
    pass
