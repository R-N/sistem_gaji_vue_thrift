from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxDepartemen, MxSubdepartemen, MxPkPeriode
from utils.util import get_cls_attr


class DbSubdepartemen(MxPkPeriode, MxSubdepartemen, DbLaporanEntity):

    perusahaan_id = get_cls_attr(MxDepartemen, 'perusahaan_id').fget(True)
    perusahaan_nama = get_cls_attr(MxPerusahaan, 'nama').fget(True)
    departemen_nama = get_cls_attr(MxDepartemen, 'nama').fget(True)

    __table_args__ = get_cls_attr(MxSubdepartemen, '__table_args__').fget(True) + get_cls_attr(MxDepartemen, '__table_args__').fget(True)

    '''
    def __init__(
        self,
        perusahaan_id,
        perusahaan_nama,
        departemen_nama,
        periode,
        *args,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.perusahaan_id = perusahaan_id
        self.perusahaan_nama = perusahaan_nama
        self.departemen_nama = departemen_nama
    '''

    def __repr__(self):
        return "%s(%s)" % (DbSubdepartemen.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
