from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr


class MxJobLevelLembur:
    @declared_attr
    def upah_lembur_1(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def upah_lembur_2(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def upah_lembur_3(cls):
        return Column(Integer, nullable=False)

    '''
    def mx_init(
        self,
        upah_lembur_1,
        upah_lembur_2,
        upah_lembur_3
    ):
        self.upah_lembur_1 = upah_lembur_1
        self.upah_lembur_2 = upah_lembur_2
        self.upah_lembur_3 = upah_lembur_3
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return ""

    @declared_attr
    def upah_lembur(cls):
        @hybrid_property
        def upah_lembur(self):
            return [self.upah_lembur_1, self.upah_lembur_2, self.upah_lembur_3]
        return upah_lembur

    def mx_init_repr(self):
        return {
            'upah_lembur_1': self.upah_lembur_1,
            'upah_lembur_2': self.upah_lembur_2,
            'upah_lembur_3': self.upah_lembur_3
        }
