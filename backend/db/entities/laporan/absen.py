from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property

from .base import DbLaporanEntity
from ..mixin import MxAbsen, MxPkPeriode, MxJobLevel
from utils.util import get_cls_attr


class DbAbsen(MxPkPeriode, MxAbsen, DbLaporanEntity):

    koef = Column(Numeric, nullable=False)
    gaji_pokok = get_cls_attr(MxJobLevel, 'gaji_pokok').fget(True)

    '''
    def __init__(
        self,
        periode,
        *args,
        gaji_pokok,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.gaji_pokok = gaji_pokok
    '''
    
    def __repr__(self):
        return "%s(%s, gaji_pokok=%r)" % (DbAbsen.__name__, self.periode_repr(), self.gaji_pokok)

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()

    @hybrid_property
    def potongan_persen(self):
        return self.get_potongan_persen(self.koef)

    @hybrid_property
    def potongan(self):
        return self.potongan_persen * self.gaji_pokok
