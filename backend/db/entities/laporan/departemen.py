from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxDepartemen, MxPkPeriode
from .mixin import MxRekapGajiDepartemen
from utils.util import get_cls_attr


class DbDepartemen(
    MxPkPeriode,
    MxRekapGajiDepartemen,
    MxDepartemen,
    DbLaporanEntity
):
    perusahaan_nama = get_cls_attr(MxPerusahaan, 'nama').fget(True)

    '''
    def __init__(
        self,
        periode,
        *args,
        perusahaan_nama,
        **kwargs
    ):
        MxDepartemen.mx_init(self, *args, **kwargs)
        self.periode_init(periode)
        self.perusahaan_nama = perusahaan_nama
    '''

    def __repr__(self):
        return "%s(%s)" % (DbDepartemen.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
