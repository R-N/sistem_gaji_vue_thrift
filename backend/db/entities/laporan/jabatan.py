from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxJobLevel, MxJabatanBase, MxPkPeriode
from utils.util import get_cls_attr


class DbJabatan(MxPkPeriode, MxJabatanBase, DbLaporanEntity):

    job_level_nama = get_cls_attr(MxJobLevel, 'nama').fget(True)

    '''
    def __init__(
        self,
        job_level_nama,
        periode,
        *args,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.job_level_nama = job_level_nama
    '''

    def __repr__(self):
        return "%s(%s)" % (DbJabatan.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
