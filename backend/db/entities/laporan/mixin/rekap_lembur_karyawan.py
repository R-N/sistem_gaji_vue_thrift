from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from ...mixin import MxJobLevelLembur

class MxRekapLemburKaryawan(MxJobLevelLembur):
    subtotal_upah_lembur = Column(Integer, nullable=False, default=0)
    total_uang_makan = Column(Integer, nullable=False, default=0)
    total_uang_transport = Column(Integer, nullable=False, default=0)

    @declared_attr
    def total_upah_lembur(cls):
        @hybrid_property
        def total_upah_lembur(self):
            return self.subtotal_upah_lembur
        return total_upah_lembur
