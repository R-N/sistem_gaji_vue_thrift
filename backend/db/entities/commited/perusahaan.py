from sqlalchemy.orm import reconstructor

from .base import DbCommitedEntity
from ..mixin import MxPerusahaan, MxCommited


class DbPerusahaan(MxCommited, MxPerusahaan, DbCommitedEntity):
    pass
