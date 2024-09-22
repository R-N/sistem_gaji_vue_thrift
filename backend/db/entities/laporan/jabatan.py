from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxJobLevel, MxJabatanBase, MxPkPeriode
from utils.util import get_cls_attr


class DbJabatan(MxPkPeriode, MxJabatanBase, DbLaporanEntity):

    job_level_name = get_cls_attr(MxJobLevel, 'name').fget(True)

    '''
    def __init__(
        self,
        job_level_name,
        periode,
        *args,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.job_level_name = job_level_name
    '''

    def __repr__(self):
        return "%s(%s)" % (DbJabatan.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
