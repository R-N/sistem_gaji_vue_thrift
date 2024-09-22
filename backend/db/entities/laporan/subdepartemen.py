from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxDepartemen, MxSubdepartemen, MxPkPeriode
from utils.util import get_cls_attr


class DbSubdepartemen(MxPkPeriode, MxSubdepartemen, DbLaporanEntity):

    perusahaan_id = get_cls_attr(MxDepartemen, 'perusahaan_id').fget(True)
    perusahaan_name = get_cls_attr(MxPerusahaan, 'name').fget(True)
    departemen_name = get_cls_attr(MxDepartemen, 'name').fget(True)

    __table_args__ = get_cls_attr(MxSubdepartemen, '__table_args__').fget(True) + get_cls_attr(MxDepartemen, '__table_args__').fget(True)

    '''
    def __init__(
        self,
        perusahaan_id,
        perusahaan_name,
        departemen_name,
        periode,
        *args,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.perusahaan_id = perusahaan_id
        self.perusahaan_name = perusahaan_name
        self.departemen_name = departemen_name
    '''

    def __repr__(self):
        return "%s(%s)" % (DbSubdepartemen.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
