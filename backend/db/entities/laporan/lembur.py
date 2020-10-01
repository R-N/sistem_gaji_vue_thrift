from sqlalchemy import Column, Integer
from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxLemburBase, MxPkPeriode


class DbLembur(MxPkPeriode, MxLemburBase, DbLaporanEntity):

    durasi_1 = Column(Integer, nullable=False, default=0)
    durasi_2 = Column(Integer, nullable=False, default=0)
    durasi_3 = Column(Integer, nullable=False, default=0)

    uang_makan = Column(Integer, nullable=False, default=0)
    uang_transport = Column(Integer, nullable=False, default=0)

    '''
    def __init__(
        self,
        periode,
        *args,
        durasi_1=0,
        durasi_2=0,
        durasi_3=0,
        uang_makan=0,
        uang_transport=0,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)

        self.durasi_1 = durasi_1
        self.durasi_2 = durasi_2
        self.durasi_3 = durasi_3
        self.uang_makan = uang_makan
        self.uang_transport = uang_transport
    '''

    def __repr__(self):
        return "%s(%s)" % (DbLembur.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
