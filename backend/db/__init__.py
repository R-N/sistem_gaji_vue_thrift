from sqlalchemy.exc import IntegrityError
from .errors import parse_db_error
from .index import connect_str, engine, session

from .entities import DbGeneralEntity, DbStagingEntity, DbCommitedEntity, DbLaporanEntity
from .validator import bind_rules, create_rules_fields
from sqlalchemy.schema import CreateSchema

import os
from dotenv import load_dotenv

load_dotenv()

def create_schemas(engine=engine):
    DB_GENERAL = os.getenv("DB_GENERAL", "sistem_gaji_general")
    DB_COMMITED = os.getenv("DB_COMMITED", "sistem_gaji_commited")
    DB_LAPORAN = os.getenv("DB_LAPORAN", "sistem_gaji_laporan")
    DB_STAGING = os.getenv("DB_STAGING", "sistem_gaji_staging")
    schemas = [DB_GENERAL, DB_COMMITED, DB_LAPORAN, DB_STAGING]
    with engine.connect() as conn:
        for schema_name in schemas:
            if not conn.dialect.has_schema(conn, schema_name):
                conn.execute(CreateSchema(schema_name))
        commit(conn)


def create_tables(engine=engine):
    DbGeneralEntity.metadata.create_all(engine)
    DbStagingEntity.metadata.create_all(engine)
    DbCommitedEntity.metadata.create_all(engine)
    DbLaporanEntity.metadata.create_all(engine)


def commit(session=session):
    try:
        session.commit()
    except IntegrityError as ex:
        parsed = parse_db_error(ex)
        if parsed:
            raise parsed
        raise

