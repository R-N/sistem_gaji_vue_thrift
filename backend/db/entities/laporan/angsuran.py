from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxAngsuran, MxPkPeriode, MxJenisAngsuran
from utils.util import get_cls_attr

class DbAngsuran(MxPkPeriode, MxAngsuran, DbLaporanEntity):
    jenis_angsuran_nama = get_cls_attr(MxJenisAngsuran, 'nama').fget(True)
    jenis_angsuran_jenis = get_cls_attr(MxJenisAngsuran, 'jenis').fget(True)

    '''
    def __init__(
        self,
        periode,
        *args,
        jenis_angsuran_nama,
        jenis_angsuran_jenis,
        **kwargs
    ):
        self.mx_init(*args, **kwargs)
        self.periode_init(periode)
        self.jenis_angsuran_nama = jenis_angsuran_nama
        self.jenis_angsuran_jenis = jenis_angsuran_jenis
    '''

    def __repr__(self):
        return "%s(%s)" % (DbAngsuran.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
