from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode


class MxSubdepartemen(MxAiId):
    __tablename__ = 'subdepartemen'


    @declared_attr
    def nama(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def departemen_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def departemen(cls):
        return relationship("DbDepartemen", back_populates="subdepartemen", uselist=False)

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="subdepartemen", viewonly=True)

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "departemen_id"]),
                pop_periode(cls, ["departemen.periode", "departemen.id"]),
                deferrable=True
            ),
        )

    def mx_init(
        self,
        departemen_id,
        nama
    ):
        self.nama = nama
        self.departemen_id = departemen_id

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, departemen_id=%r, nama=%r" % (self.id, self.departemen_id, self.nama)
