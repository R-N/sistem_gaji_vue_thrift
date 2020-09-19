from sqlalchemy.exc import IntegrityError
from .errors import parse_db_error
from .index import connect_str, engine, DBEntity, db_session, create_tables

def db_commit():
    try:
        db_session.commit()
    except IntegrityError as ex:
        parsed = parse_db_error(ex)
        if parsed:
            raise parsed
        raise

commit = db_commit
session = db_session
Entity = DBEntity