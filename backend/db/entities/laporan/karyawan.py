from sqlalchemy.orm import reconstructor

from .base import DbLaporanEntity
from ..mixin import MxPerusahaan, MxDepartemen, MxSubdepartemen, MxJobLevel, MxJabatan, MxKaryawanBase, MxPkPeriode, MxKaryawan
from .mixin import MxSlipGajiKaryawan, MxUpahLemburKaryawan, MxRekapLemburKaryawan, MxPotonganAbsenKaryawan, MxRekapAbsenKaryawan
from utils.util import get_cls_attr


class DbKaryawan(
    MxPkPeriode,
    MxSlipGajiKaryawan,
    MxPotonganAbsenKaryawan,
    MxRekapAbsenKaryawan,
    MxUpahLemburKaryawan,
    MxRekapLemburKaryawan,
    MxKaryawanBase,
    DbLaporanEntity
):

    perusahaan_id = get_cls_attr(MxDepartemen, 'perusahaan_id').fget(True)
    perusahaan_name = get_cls_attr(MxPerusahaan, 'name').fget(True)
    departemen_id = get_cls_attr(MxSubdepartemen, 'departemen_id').fget(True)
    departemen_name = get_cls_attr(MxDepartemen, 'name').fget(True)
    subdepartemen_name = get_cls_attr(MxSubdepartemen, 'name').fget(True)
    job_level_id = get_cls_attr(MxJabatan, 'job_level_id').fget(True)
    job_level_name = get_cls_attr(MxJobLevel, 'name').fget(True)
    jabatan_name = get_cls_attr(MxJabatan, 'name').fget(True)

    __table_args__ = get_cls_attr(MxKaryawan, '__table_args__').fget(True) + get_cls_attr(MxJabatan, '__table_args__').fget(True) + get_cls_attr(MxSubdepartemen, '__table_args__').fget(True) + get_cls_attr(MxDepartemen, '__table_args__').fget(True)

    '''
    def __init__(
        self,
        perusahaan_name,
        periode,
        *args,
        **kwargs
    ):
        self.periode_init(periode)
        self.no_induk = no_induk
        self.name = name
        self.perusahaan_id = perusahaan_id
        self.perusahaan_name = perusahaan_name
    '''

    def __repr__(self):
        return "%s(%s)" % (DbKaryawan.__name__, self.periode_repr())

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
