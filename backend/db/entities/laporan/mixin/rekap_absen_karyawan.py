from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr

class MxRekapAbsenKaryawan:
    jam_1 = Column(Integer, nullable=False, default=0)
    jam_2 = Column(Integer, nullable=False, default=0)
    jam_3 = Column(Integer, nullable=False, default=0)
    jam_4 = Column(Integer, nullable=False, default=0)
    jam_5 = Column(Integer, nullable=False, default=0)
    jam_6 = Column(Integer, nullable=False, default=0)
    jam_7 = Column(Integer, nullable=False, default=0)
    jam_8 = Column(Integer, nullable=False, default=0)

    total_jam = Column(Integer, nullable=False, default=0)
    total_potongan = Column(Integer, nullable=False, default=0)

    koef_jam = [1, 2, 3, 4, 5, 6, 7, 8]

    @declared_attr
    def jam(cls):
        @hybrid_property
        def jam(self):
            return [
                self.jam_1,
                self.jam_2,
                self.jam_3,
                self.jam_4,
                self.jam_5,
                self.jam_6,
                self.jam_7,
                self.jam_8
            ]
        return jam

    '''
    @declared_attr
    def total_jam(cls):
        @hybrid_property
        def total_jam(self):
            jam = self.jam
            return sum([jam[i] * MxRekapAbsenKaryawan.koef_jam[i] for i in range(0, 8)])
        return total_jam
    '''

