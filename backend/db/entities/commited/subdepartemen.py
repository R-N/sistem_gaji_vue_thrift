from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxSubdepartemen, MxCommited


class DbSubdepartemen(MxCommited, MxSubdepartemen, DbCommitedEntity):
    pass
