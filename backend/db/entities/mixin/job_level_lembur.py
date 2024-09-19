from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from rpc.gen.data.job_level.errors.ttypes import TJobLevelError, TJobLevelErrorCode


class MxJobLevelLembur:
    @declared_attr
    def _upah_lembur_1(cls):
        return Column("upah_lembur_1", Integer, nullable=False, default=0)

    @declared_attr
    def _upah_lembur_2(cls):
        return Column("upah_lembur_2", Integer, nullable=False, default=0)

    @declared_attr
    def _upah_lembur_3(cls):
        return Column("upah_lembur_3", Integer, nullable=False, default=0)

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

    # Properties and other methods associated with columns

    # upah_lembur

    @declared_attr
    def upah_lembur_1(cls):
        @hybrid_property
        def upah_lembur_1(self):
            return self._upah_lembur_1

        @upah_lembur_1.setter
        def upah_lembur_1(self, upah_lembur):
            DbJobLevelLemburValidator.validate_upah_lembur(upah_lembur, 1)
            self._upah_lembur_1 = upah_lembur

        return upah_lembur_1

    @declared_attr
    def upah_lembur_2(cls):
        @hybrid_property
        def upah_lembur_2(self):
            return self._upah_lembur_2

        @upah_lembur_2.setter
        def upah_lembur_2(self, upah_lembur):
            DbJobLevelLemburValidator.validate_upah_lembur(upah_lembur, 2)
            self._upah_lembur_2 = upah_lembur

        return upah_lembur_2

    @declared_attr
    def upah_lembur_3(cls):
        @hybrid_property
        def upah_lembur_3(self):
            return self._upah_lembur_3

        @upah_lembur_3.setter
        def upah_lembur_3(self, upah_lembur):
            DbJobLevelLemburValidator.validate_upah_lembur(upah_lembur, 3)
            self._upah_lembur_3 = upah_lembur

        return upah_lembur_3

    # Other methods

    def fill_lembur(self, obj):
        obj.upah_lembur_1 = self.upah_lembur_1
        obj.upah_lembur_2 = self.upah_lembur_2
        obj.upah_lembur_3 = self.upah_lembur_3

        return obj
    
    def fill(self, obj):
        return self.fill_lembur(obj)

    # validator

    def validator():
        return DbJobLevelLemburValidator

class DbJobLevelLemburValidator:

    def validate_upah_lembur(upah_lembur, i):
        if not isinstance(upah_lembur, int) or upah_lembur < 0:
            raise TJobLevelError(TJobLevelErrorCode.UPAH_LEMBUR_INVALID_2 % i)
