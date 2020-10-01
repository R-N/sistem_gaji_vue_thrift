from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from .job_level_base import MxJobLevelBase
from .job_level_lembur import MxJobLevelLembur


class MxJobLevel(MxJobLevelBase, MxJobLevelLembur):
    @declared_attr
    def gaji_pokok(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def tunjangan_jabatan(cls):
        return Column(Integer, nullable=False)

    @declared_attr
    def tunjangan_kinerja(cls):
        return relationship("DbTunjanganKinerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganKinerja.kinerja")

    @declared_attr
    def tunjangan_masa_kerja(cls):
        return relationship("DbTunjanganMasaKerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganMasaKerja.batas_bawah")

    '''
    def mx_init(
        self,
        *args,
        gaji_pokok,
        tunjangan_jabatan,
        upah_lembur_1,
        upah_lembur_2,
        upah_lembur_3,
        **kwargs
    ):
        MxJobLevelBase.mx_init(self, *args, **kwargs)
        MxJobLevelLembur.mx_init(self, upah_lembur_1, upah_lembur_2, upah_lembur_3)
        self.gaji_pokok = gaji_pokok
        self.tunjangan_jabatan = tunjangan_jabatan
    '''

    def mx_reconstruct(self):
        MxJobLevelBase.mx_reconstruct(self)

    def mx_repr(self):
        return "%s, gaji_pokok=%r, tunjangan_jabatan=%r" % (MxJobLevelBase.mx_repr(self), self.gaji_pokok, self.tunjangan_jabatan)

    def mx_init_repr(self):
        ret = MxJobLevelBase.mx_init_repr(self)
        ret.update(MxJobLevelLembur.mx_init_repr(self))
        ret.update({
            'gaji_pokok': self.gaji_pokok,
            'tunjangan_jabatan': self.tunjangan_jabatan
        })
        return ret
