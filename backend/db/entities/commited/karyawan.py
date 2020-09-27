from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxKaryawan, MxCommited


class DbKaryawan(MxCommited, MxKaryawan, DbCommitedEntity):
    pass
