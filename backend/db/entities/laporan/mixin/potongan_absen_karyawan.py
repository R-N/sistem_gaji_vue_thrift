from sqlalchemy import Column, Numeric
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from ...mixin import MxAbsen


class MxPotonganAbsenKaryawan:
    koef_absen = Column(Numeric, nullable=False)

    @declared_attr
    def get_potongan_persen(cls):
        @hybrid_method
        def get_potongan_persen(self, jam):
            return self.koef_absen * (1+jam)
        return get_potongan_persen

    @declared_attr
    def potongan_persen(cls):
        @hybrid_property
        def potongan_persen(self):
            return [self.get_potongan_persen(j) for j in range(0, 8)]
        return potongan_persen

    @declared_attr
    def potongan(cls):
        @hybrid_property
        def potongan(self):
            return [p * self.gaji_pokok for p in self.potongan_persen]
        return potongan

    @declared_attr
    def get_potongan(cls):
        @hybrid_method
        def get_potongan(self, jam):
            return self.get_potongan_persen(jam) * self.gaji_pokok
        return get_potongan
