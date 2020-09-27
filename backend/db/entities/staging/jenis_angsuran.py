from sqlalchemy.orm import reconstructor

from .base import DbStagingEntity
from ..mixin import MxJenisAngsuran, MxStaging


class DbJenisAngsuran(MxStaging, MxJenisAngsuran, DbStagingEntity):
    pass
