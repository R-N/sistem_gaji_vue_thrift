from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr


class MxShiftBase:
    __tablename__ = 'shift'
    @declared_attr
    def kode(cls):
        return Column(String(6), primary_key=True)

    @declared_attr
    def lembur(cls):
        return relationship("DbLembur", back_populates="shift_rel", viewonly=True, passive_deletes="all")

    '''
    def mx_init(
        self,
        kode
    ):
        self.kode = kode
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "kode=%r" % (self.kode,)

    @declared_attr
    def max_lembur(cls):
        @hybrid_property
        def max_lembur(self):
            return [self.max_lembur_1, self.max_lembur_2, self.max_lembur_3]
        return max_lembur

    def mx_init_repr(self):
        return {
            'kode': self.kode
        }
