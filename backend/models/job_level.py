from sqlalchemy.exc import IntegrityError

from rpc.gen.data.job_level.structs.ttypes import TJobLevelForm, TJobLevel
from rpc.gen.data.job_level.errors.ttypes import TJobLevelError, TJobLevelErrorCode

import db
from db.entities.staging import DbJobLevel
from db.errors import UniqueError

class JobLevelModel:
    def __init__(self):
        pass

    def parse_error(self, parsed):
        if isinstance(parsed, UniqueError):
            if parsed.column == "name":
                raise TJobLevelError(TJobLevelErrorCode.NAME_ALREADY_EXISTS)

    def commit(self):
        try:
            db.commit()
        except IntegrityError as ex:
            self.parse_error(ex)
            raise

    def fetch(self, query=None):
        db_query = db.session.query(DbJobLevel)
        db_query = db_query.order_by(DbJobLevel.enabled.desc(), DbJobLevel.name.asc())
        if query:
            if query.enabled is not None:
                db_query = db_query.filter(DbJobLevel.enabled == query.enabled)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        return db_query.all()

    def get(self, job_level_id):
        joblevel = db.session.query(DbJobLevel).filter(DbJobLevel.id == job_level_id).scalar()
        if not joblevel:
            raise TJobLevelError(TJobLevelErrorCode.JOBLEVEL_NOT_FOUND)
        return joblevel

    def create(self, form):
        job_level = DbJobLevel()
        job_level.name = form.name

        db.session.add(job_level)
        return job_level

    def set_enabled(self, job_level, enabled):
        job_level.enabled = enabled
        db.session.add(job_level)

    def set_name(self, job_level, name):
        job_level.name = name
        db.session.add(job_level)

    def set_gaji_pokok(self, job_level, gaji_pokok):
        job_level.gaji_pokok = gaji_pokok
        db.session.add(job_level)

    def set_tunjangan_jabatan(self, job_level, tunjangan_jabatan):
        job_level.tunjangan_jabatan = tunjangan_jabatan
        db.session.add(job_level)

    def set_upah_lembur_1(self, job_level, upah_lembur):
        job_level.upah_lembur_1 = upah_lembur
        db.session.add(job_level)

    def set_upah_lembur_2(self, job_level, upah_lembur):
        job_level.upah_lembur_2 = upah_lembur
        db.session.add(job_level)

    def set_upah_lembur_3(self, job_level, upah_lembur):
        job_level.upah_lembur_3 = upah_lembur
        db.session.add(job_level)

    def set_upah_lembur(self, job_level, upah_lembur, i):
        setattr(job_level, f"upah_lembur_{i}", upah_lembur)
        getattr(self, f"set_upah_lembur_{i}")(job_level, upah_lembur)
        db.session.add(job_level)
