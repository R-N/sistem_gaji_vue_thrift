from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode, eager_load_staging_parent


class MxSubdepartemen(MxAiId):
    __tablename__ = 'subdepartemen'


    @declared_attr
    def name(cls):
        return Column(String(50), nullable=False)

    @declared_attr
    def departemen_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def departemen(cls):
        return relationship(
            "DbDepartemen",
            back_populates="subdepartemen",
            uselist=False,
            lazy=eager_load_staging_parent(cls)
        )

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="subdepartemen", viewonly=True, passive_deletes="all")

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "departemen_id"]),
                pop_periode(cls, ["departemen.periode", "departemen.id"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

    '''
    def mx_init(
        self,
        id,
        departemen_id,
        name
    ):
        self.name = name
        self.departemen_id = departemen_id
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, departemen_id=%r, name=%r" % (self.id, self.departemen_id, self.name)


    def mx_init_repr(self):
        return {
            'departemen_id': self.departemen_id,
            'name': self.name,
            'id': self.id
        }