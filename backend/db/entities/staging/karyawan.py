from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxKaryawan, MxStaging


class DbKaryawan(MxStaging, MxKaryawan, DbStagingEntity):
    pass
