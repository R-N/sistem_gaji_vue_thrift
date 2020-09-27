from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxKinerja, MxStaging


class DbKinerja(MxStaging, MxKinerja, DbStagingEntity):
    pass
