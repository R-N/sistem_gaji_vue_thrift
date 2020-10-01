from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPeriodeGaji, MxRepr


class DbPeriodeGaji(MxRepr, MxPeriodeGaji, DbLaporanEntity):
    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
