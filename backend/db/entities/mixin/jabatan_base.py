from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import MxAiId, pop_periode, eager_load_staging_parent
from .secondary import ScTunjanganKhususJabatan


class MxJabatanBase(MxAiId):
    __tablename__ = 'jabatan'

    @declared_attr
    def name(cls):
        return Column(String(50), unique=True, nullable=False)

    @declared_attr
    def job_level_id(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def job_level(cls):
        return relationship(
            "DbJobLevel",
            back_populates="jabatan",
            uselist=False,
            lazy=eager_load_staging_parent(cls)
        )

    @declared_attr
    def karyawan(cls):
        return relationship("DbKaryawan", back_populates="jabatan", viewonly=True, passive_deletes="all")

    @declared_attr
    def __table_args__(cls):
        return (
            ForeignKeyConstraint(
                pop_periode(cls, ["periode", "job_level_id"]),
                pop_periode(cls, ["job_level.periode", "job_level.id"]),
                deferrable=True,
                ondelete="RESTRICT",
            ),
        )

    '''
    def mx_init(
        self,
        id,
        job_level_id,
        name
    ):
        self.name = name
        self.job_level_id = job_level_id
        self.id_init(id)
    '''

    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return "id=%r, job_level_id=%r, name=%r" % (self.id, self.job_level_id, self.name)

    def mx_init_repr(self):
        return {
            'job_level_id': self.job_level_id,
            'name': self.name,
            'id': self.id
        }
