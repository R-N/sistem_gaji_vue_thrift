from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxJenisAngsuran, MxCommited


class DbJenisAngsuran(MxCommited, MxJenisAngsuran, DbCommitedEntity):
    pass
