from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from .shift_base import MxShiftBase


class MxShift(MxShiftBase):

    @declared_attr
    def max_lembur_1(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def max_lembur_2(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def max_lembur_3(cls):
        return Column(Integer, nullable=False, default=24)

    '''
    def mx_init(
        self,
        *args,
        max_lembur_1,
        max_lembur_2,
        max_lembur_3,
        **kwargs
    ):
        MxShiftBase.mx_init(self, *args, **kwargs)
        self.max_lembur_1 = max_lembur_1
        self.max_lembur_2 = max_lembur_2
        self.max_lembur_3 = max_lembur_3
    '''

    def mx_reconstruct(self):
        MxShiftBase.mx_reconstruct(self)

    def mx_repr(self):
        return "%s, max_lembur_1=%r, max_lembur_2=%r, max_lembur_3=%r" % (MxShiftBase.mx_repr(self), self.max_lembur_1, self.max_lembur_2, self.max_lembur_3)

    @declared_attr
    def max_lembur(cls):
        @hybrid_property
        def max_lembur(self):
            return [self.max_lembur_1, self.max_lembur_2, self.max_lembur_3]
        return max_lembur

    def mx_init_repr(self):
        ret = MxShiftBase.mx_init_repr(self)
        ret.update({
            'max_lembur_1': self.max_lembur_1,
            'max_lembur_2': self.max_lembur_2,
            'max_lembur_3': self.max_lembur_3
        })
        return ret
