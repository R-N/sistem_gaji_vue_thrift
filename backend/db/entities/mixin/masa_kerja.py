from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class MxMasaKerja:
    __tablename__ = 'masa_kerja'

    @declared_attr
    def nilai(cls):
        return Column(Integer, primary_key=True, nullable=False)

    '''
    def mx_init(
        self,
        nilai
    ):
        self.nilai = nilai
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "nilai=%r" % (self.nilai,)

    def mx_init_repr(self):
        return {
            'nilai': self.nilai
        }
