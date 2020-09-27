from sqlalchemy.exc import IntegrityError
from .errors import parse_db_error
from .index import connect_str, engine, session

from .entities import DbGeneralEntity
from .entities import DbStagingEntity
from .entities import DbCommitedEntity


def create_tables(engine=engine):
    DbGeneralEntity.metadata.create_all(engine)
    DbStagingEntity.metadata.create_all(engine)
    DbCommitedEntity.metadata.create_all(engine)


def commit(session=session):
    try:
        session.commit()
    except IntegrityError as ex:
        parsed = parse_db_error(ex)
        if parsed:
            raise parsed
        raise

