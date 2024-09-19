from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from .job_level_base import MxJobLevelBase, DbJobLevelBaseValidator
from .job_level_lembur import MxJobLevelLembur, DbJobLevelLemburValidator
from rpc.gen.data.job_level.errors.ttypes import TJobLevelError, TJobLevelErrorCode


class MxJobLevel(MxJobLevelBase, MxJobLevelLembur):
    @declared_attr
    def _gaji_pokok(cls):
        return Column("gaji_pokok", Integer, nullable=False, default=0)

    @declared_attr
    def _tunjangan_jabatan(cls):
        return Column("tunjangan_jabatan", Integer, nullable=False, default=0)

    @declared_attr
    def tunjangan_kinerja(cls):
        return relationship("DbTunjanganKinerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganKinerja.kinerja", passive_deletes="all")

    @declared_attr
    def tunjangan_masa_kerja(cls):
        return relationship("DbTunjanganMasaKerja", back_populates="job_level", viewonly=True, order_by="DbTunjanganMasaKerja.batas_bawah", passive_deletes="all")

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

    # Properties and other methods associated with columns

    # gaji_pokok

    @declared_attr
    def gaji_pokok(cls):
        @hybrid_property
        def gaji_pokok(self):
            return self._gaji_pokok

        @gaji_pokok.setter
        def gaji_pokok(self, gaji_pokok):
            DbJobLevelLemburValidator.validate_gaji_pokok(gaji_pokok)
            self._gaji_pokok = gaji_pokok

        return gaji_pokok

    # tunjangan_jabatan

    @declared_attr
    def tunjangan_jabatan(cls):
        @hybrid_property
        def tunjangan_jabatan(self):
            return self._tunjangan_jabatan

        @tunjangan_jabatan.setter
        def tunjangan_jabatan(self, nama):
            DbJobLevelLemburValidator.validate_upah_lembur(nama)
            self._tunjangan_jabatan = tunjangan_jabatan

        return tunjangan_jabatan

    # Other methods

    def fill(self, obj):
        obj = self.fill_base(obj)
        obj.gaji_pokok = self.gaji_pokok
        obj.tunjangan_jabatan = self.tunjangan_jabatan
        obj = self.fill_lembur(obj)

        return obj

    # validator

    def validator():
        return DbJobLevelLemburValidator

class DbJobLevelLemburValidator(DbJobLevelBaseValidator, DbJobLevelLemburValidator):
    def validate_gaji_pokok(gaji_pokok):
        if not isinstance(gaji_pokok, int) or gaji_pokok < 0:
            raise TJobLevelError(TJobLevelErrorCode.GAJI_POKOK_INVALID)

    def validate_tunjangan_jabatan(tunjangan_jabatan):
        if not isinstance(tunjangan_jabatan, int) or tunjangan_jabatan < 0:
            raise TJobLevelError(TJobLevelErrorCode.TUNJANGAN_JABATAN_INVALID)
