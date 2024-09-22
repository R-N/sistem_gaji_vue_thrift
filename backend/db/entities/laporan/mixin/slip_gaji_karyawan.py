from sqlalchemy import Column, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from ...mixin import MxKaryawan, MxJobLevel, MxTunjanganKinerja, MxPengaturanBase, MxPeriodeGaji, MxTunjanganKhusus, MxPengaturan
from utils.util import get_cls_attr

class MxSlipGajiKaryawan:
    no_slip = Column(Integer, nullable=False)

    kinerja = get_cls_attr(MxKaryawan, 'kinerja').fget(True)
    kinerja_rel = get_cls_attr(MxKaryawan, 'kinerja_rel')
    gaji_pokok = get_cls_attr(MxJobLevel, 'gaji_pokok').fget(True)
    tunjangan_jabatan = get_cls_attr(MxJobLevel, 'tunjangan_jabatan').fget(True)
    tunjangan_kinerja = get_cls_attr(MxTunjanganKinerja, 'nilai').fget(True)

    tunjangan_khusus = get_cls_attr(MxTunjanganKhusus, 'nilai').fget(True)
    thr = get_cls_attr(MxKaryawan, 'thr').fget(True)
    lain_lain = get_cls_attr(MxKaryawan, 'lain_lain').fget(True)

    pph_21_pot = get_cls_attr(MxKaryawan, 'pph_21').fget(True)

    bpjs_ketenagakerjaan_kar = Column(Integer, nullable=False)
    bpjs_kesehatan_kar = Column(Integer, nullable=False)

    # total_upah_lembur = Column(Integer, nullable=False, default=0)  # sudah ada dari rekap upah lembur
    insentif = Column(Integer, nullable=False, default=0)

    bpjs_ketenagakerjaan_pot = Column(Integer, nullable=False)
    bpjs_kesehatan_pot = Column(Integer, nullable=False)

    iuran_rumah_pot = get_cls_attr(MxPengaturan, 'iuran_rumah').fget(True)
    iuran_koperasi_pot = get_cls_attr(MxPengaturan, 'pendaftaran_koperasi').fget(True)
    total_angsuran_koperasi_pot = Column(Integer, nullable=False, default=0)
    total_angsuran_bank_pot = Column(Integer, nullable=False, default=0)
    total_absen_pot = Column(Integer, nullable=False, default=0)

    # name_mengetahui = get_cls_attr(MxPengaturanBase, 'name_mengetahui').fget(True)
    # name_pembuat = get_cls_attr(MxPeriodeGaji, 'pengubah_name').fget(True)

    '''
    def mx_init(
        self,
        no_slip,
        kinerja,
        gaji_pokok,
        tunjangan_jabatan,
        tunjangan_kinerja,
        pph_21_pot,
        bpjs_ketenagakerjaan_kar,
        bpjs_kesehatan_kar,
        bpjs_ketenagakerjaan_pot,
        bpjs_kesehatan_pot,
        tunjangan_khusus=0,
        thr=0,
        lain_lain=0,
        # total_upah_lembur=0,
        insentif=0,
        iuran_rumah_pot=0,
        iuran_koperasi_pot=0,
        total_angsuran_koperasi_pot=0,
        total_angsuran_bank_pot=0,
        total_absen_pot=0
    ):
        self.no_slip = no_slip
        self.kinerja = kinerja
        self.gaji_pokok = gaji_pokok
        self.tunjangan_jabatan = tunjangan_jabatan
        self.tunjangan_kinerja = tunjangan_kinerja

        self.pph_21_pot = pph_21_pot

        self.bpjs_ketenagakerjaan_kar = bpjs_ketenagakerjaan_kar
        self.bpjs_kesehatan_kar = bpjs_kesehatan_kar

        self.bpjs_ketenagakerjaan_pot = bpjs_ketenagakerjaan_pot
        self.bpjs_kesehatan_pot = bpjs_kesehatan_pot

        self.tunjangan_khusus = tunjangan_khusus
        self.thr = thr
        self.lain_lain = lain_lain

        # self.total_upah_lembur = total_upah_lembur
        self.insentif = insentif

        self.iuran_rumah_pot = iuran_rumah_pot
        self.iuran_koperasi_pot = iuran_koperasi_pot
        self.total_angsuran_koperasi_pot = total_angsuran_koperasi_pot
        self.total_angsuran_bank_pot = total_angsuran_bank_pot
        self.total_absen_pot = total_absen_pot
    '''
    
    def mx_reconstruct(self):
        pass

    def mx_repr(self):
        return ""

    def mx_init_repr(self):
        return {
            'no_slip': self.no_slip,
            'kinerja': self.kinerja,
            'gaji_pokok': self.gaji_pokok,
            'tunjangan_jabatan': self.tunjangan_jabatan,
            'tunjangan_kinerja': self.tunjangan_kinerja,
            'pph_21_pot': self.pph_21_pot,
            'bpjs_ketenagakerjaan_kar': self.bpjs_ketenagakerjaan_kar,
            'bpjs_kesehatan_kar': self.bpjs_kesehatan_kar,
            'bpjs_ketenagakerjaan_pot': self.bpjs_ketenagakerjaan_pot,
            'bpjs_kesehatan_pot': self.bpjs_kesehatan_pot,
            'tunjangan_khusus': self.tunjangan_khusus,
            'thr': self.thr,
            'lain_lain': self.lain_lain,
            # 'total_upah_lembur': self.total_upah_lembur,
            'insentif': self.insentif,
            'iuran_rumah_pot': self.iuran_rumah_pot,
            'iuran_koperasi_pot': self.iuran_koperasi_pot,
            'total_angsuran_koperasi_pot': self.total_angsuran_koperasi_pot,
            'total_angsuran_bank_pot': self.total_angsuran_bank_pot,
            'total_absen_pot': self.total_absen_pot
        }

    @declared_attr
    def total_koperasi_pot(cls):
        @hybrid_property
        def total_koperasi_pot(self):
            return self.iuran_koperasi_pot + self.total_angsuran_koperasi_pot
        return total_koperasi_pot

    @declared_attr
    def total_bank_pot(cls):
        @hybrid_property
        def total_bank_pot(self):
            return self.total_angsuran_bank_pot
        return total_bank_pot

    @declared_attr
    def total_upah_lembur_insentif(cls):
        @hybrid_property
        def total_upah_lembur_insentif(self):
            return self.total_upah_lembur + self.insentif
        return total_upah_lembur_insentif

    @declared_attr
    def total_lain_lain(cls):
        @hybrid_property
        def total_lain_lain(self):
            return self.lain_lain + self.thr
        return total_lain_lain

    @declared_attr
    def total_absen_pph_21_pot(cls):
        @hybrid_property
        def total_absen_pph_21_pot(self):
            return self.total_absen_pot + self.pph_21_pot
        return total_absen_pph_21_pot

    @declared_attr
    def total_gaji(cls):
        @hybrid_property
        def total_gaji(self):
            return self.gaji_pokok + self.tunjangan_jabatan + self.tunjangan_khusus + self.tunjangan_kinerja + self.bpjs_ketenagakerjaan_kar + self.bpjs_kesehatan_kar + self.total_upah_lembur_insentif + self.total_lain_lain
        return total_gaji

    @declared_attr
    def total_pot(cls):
        @hybrid_property
        def total_pot(self):
            return self.bpjs_ketenagakerjaan_pot + self.total_koperasi_pot + self.iuran_rumah_pot + self.total_bank_pot + self.total_absen_pph_21_pot + self.bpjs_kesehatan_pot
        return total_pot
