from sqlalchemy.exc import IntegrityError

from rpc.gen.data.perusahaan.structs.ttypes import TPerusahaanForm, TPerusahaan
from rpc.gen.data.perusahaan.errors.ttypes import TPerusahaanError, TPerusahaanErrorCode

import db
from db.entities.staging import DbPerusahaan
import validators.perusahaan as validator

class PerusahaanModel:
    def __init__(self):
        self.validator = validator

    def parse_error(self, ex):
        validator.parse_error(ex)

    def commit(self):
        try:
            db.commit()
        except IntegrityError as ex:
            self.parse_error(ex)
            raise

    def fetch(self, query=None):
        db_query = db.session.query(DbPerusahaan)
        db_query = db_query.order_by(DbPerusahaan.enabled.desc(), DbPerusahaan.nama.asc())
        if query:
            if query.enabled is not None:
                db_query = db_query.filter(DbPerusahaan.enabled == query.enabled)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        return db_query.all()

    def get(self, perusahaan_id):
        perusahaan = db.session.query(DbPerusahaan).filter(DbPerusahaan.id == perusahaan_id).scalar()
        if not perusahaan:
            raise TPerusahaanError(TPerusahaanErrorCode.PERUSAHAAN_NOT_FOUND)
        return perusahaan

    def create(self, form):
        perusahaan = DbPerusahaan()
        perusahaan.set_nama(form.nama)
        db.session.add(perusahaan)
        return perusahaan

    def set_enabled(self, perusahaan, enabled):
        perusahaan.set_enabled(enabled)
        db.session.add(perusahaan)

    def set_nama(self, perusahaan, nama):
        perusahaan.set_nama(nama)
        db.session.add(perusahaan)

