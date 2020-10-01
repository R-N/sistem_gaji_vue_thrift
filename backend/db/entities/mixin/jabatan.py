from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from .secondary import ScTunjanganKhususJabatan
from .jabatan_base import MxJabatanBase


class MxJabatan(MxJabatanBase):

    @declared_attr
    def ScTunjanganKhususJabatan(cls):
        return ScTunjanganKhususJabatan(cls.metadata, cls)

    @declared_attr
    def tunjangan_khusus(cls):
        return relationship("DbTunjanganKhusus", back_populates="jabatan", secondary=lambda: cls.ScTunjanganKhususJabatan)

    @declared_attr
    def tunjangan_khusus_enabled(cls):
        @hybrid_property
        def tunjangan_khusus_aktif(self):
            return [tkh for tkh in self.tunjangan_khusus if tkh.real_enabled]

        return tunjangan_khusus_aktif

    '''
    def mx_init(
        self,
        *args,
        **kwargs
    ):
        MxJabatanBase.mx_init(self, *args, **kwargs)
    '''
