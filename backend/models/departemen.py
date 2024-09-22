from sqlalchemy.exc import IntegrityError

from rpc.gen.data.departemen.structs.ttypes import TDepartemenForm, TDepartemen
from rpc.gen.data.departemen.errors.ttypes import TDepartemenError, TDepartemenErrorCode

import db
from db.entities.staging import DbDepartemen
from db.errors import UniqueError

class DepartemenModel:
    def __init__(self):
        pass

    def parse_error(self, parsed):
        if isinstance(parsed, UniqueError):
            if parsed.column == "name":
                raise TDepartemenError(TDepartemenErrorCode.NAME_ALREADY_EXISTS)

    def commit(self):
        try:
            db.commit()
        except IntegrityError as ex:
            self.parse_error(ex)
            raise

    def fetch(self, query=None):
        db_query = db.session.query(DbDepartemen)
        if query:
            if query.perusahaan_id:
                db_query = db_query.filter(DbDepartemen.perusahaan_id == query.perusahaan_id)
        db_query = db_query.order_by(DbDepartemen.enabled.desc(), DbDepartemen.name.asc())
        if query:
            if query.enabled is not None:
                db_query = db_query.filter(DbDepartemen.enabled == query.enabled)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        return db_query.all()

    def get(self, departemen_id):
        departemen = db.session.query(DbDepartemen).filter(DbDepartemen.id == departemen_id).scalar()
        if not departemen:
            raise TDepartemenError(TDepartemenErrorCode.PERUSAHAAN_NOT_FOUND)
        return departemen

    def create(self, form):
        departemen = DbDepartemen()
        departemen.name = form.name
        departemen.perusahaan_id = form.perusahaan_id

        db.session.add(departemen)
        return departemen

    def set_enabled(self, departemen, enabled):
        departemen.enabled = enabled
        db.session.add(departemen)

    def set_name(self, departemen, name):
        departemen.name = name
        db.session.add(departemen)

