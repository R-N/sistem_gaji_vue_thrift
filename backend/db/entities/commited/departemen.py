from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxDepartemen, MxCommited


class DbDepartemen(MxCommited, MxDepartemen, DbCommitedEntity):
    pass
