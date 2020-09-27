from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode


class MxTunjanganKinerja:
    __tablename__ = 'tunjangan_kinerja'

    @declared_attr
    def job_level_id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def kinerja(cls):
        return Column(String(1), primary_key=True)
    # PK job_level_id & kinerja

    @declared_attr
    def nilai(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def job_level(cls):
        return relationship("DbJobLevel", back_populates="tunjangan_kinerja", uselist=False)

    @declared_attr
    def kinerja_rel(cls):
        return relationship("DbKinerja", uselist=False)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "job_level_id"]),
                pop_periode(cls, ["job_level.periode", "job_level.id"]),
                deferrable=True
            ),
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "kinerja"]),
                pop_periode(cls, ["kinerja.periode", "kinerja.kode"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        job_level_id,
        kinerja,
        nilai
    ):
        self.job_level_id = job_level_id
        self.kinerja = kinerja
        self.nilai = nilai

    def mx_reconstruct(self):
        pass

    def mx_init(self):
        return "id=%r, job_level_id=%r, kinerja=%r, nilai=%r)>" % (self.id, self.job_level_id, self.kinerja, self.nilai)
