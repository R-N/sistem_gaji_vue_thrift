from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .secondary import ScTunjanganKhususJabatan
from .jabatan_base import MxJabatanBase


class MxJabatan(MxJabatanBase):

    @declared_attr
    def ScTunjanganKhususJabatan(cls):
        return ScTunjanganKhususJabatan(cls.metadata, cls)

    @declared_attr
    def tunjangan_khusus(cls):
        return relationship("DbTunjanganKhusus", back_populates="jabatan", secondary=lambda: cls.ScTunjanganKhususJabatan)

    '''
    def mx_init(
        self,
        *args,
        **kwargs
    ):
        MxJabatanBase.mx_init(self, *args, **kwargs)
    '''
