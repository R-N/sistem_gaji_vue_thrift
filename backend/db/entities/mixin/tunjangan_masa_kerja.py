from sqlalchemy import Column, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxTunjanganMasaKerja:
    __tablename__ = 'tunjangan_masa_kerja'

    @declared_attr
    def job_level_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def batas_bawah(cls):
        return Column(Integer, primary_key=True)
    # PK job_level_id & batas_bawah

    @declared_attr
    def batas_atas(cls):
        return Column(Integer, nullable=True)

    @declared_attr
    def nilai(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def job_level(cls):
        return relationship("DbJobLevel", back_populates="tunjangan_masa_kerja", uselist=False)

    @declared_attr
    def batas_bawah_rel(cls):
        return relationship("DbMasaKerja", foreign_keys=[cls.batas_bawah], uselist=False)

    @declared_attr
    def batas_atas_rel(cls):
        return relationship("DbMasaKerja", foreign_keys=[cls.batas_atas], uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "job_level_id"]),
                pop_periode(cls, ["job_level.periode", "job_level.id"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "batas_bawah"]),
                pop_periode(cls, ["masa_kerja.periode", "masa_kerja.nilai"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "batas_atas"]),
                pop_periode(cls, ["masa_kerja.periode", "masa_kerja.nilai"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

    '''
    def mx_init(
        self,
        job_level_id,
        batas_bawah,
        batas_atas,
        nilai
    ):
        self.job_level_id = job_level_id
        self.batas_bawah = batas_bawah
        self.batas_atas = batas_atas
        self.nilai = nilai
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, job_level_id=%r, batas_bawah=%r, batas_atas=%r, nilai=%r" % (self.id, self.job_level_id, self.batas_bawah, self.batas_atas, self.nilai)

    def mx_init_repr(self):
        return {
            'job_level_id': self.job_level_id,
            'batas_bawah': self.batas_bawah,
            'batas_atas': self.batas_atas,
            'nilai': self.nilai
        }
