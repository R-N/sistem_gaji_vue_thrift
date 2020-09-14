from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

connect_str = "postgresql+psycopg2://%s:%s@%s:%s/%s"
connect_str = connect_str % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
engine = create_engine(connect_str)

DBEntity = declarative_base()

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def Session(scopefunc=None):
    if scopefunc:
        return scoped_session(session_factory, scopefunc=scopefunc)
    else:
        return scoped_session(session_factory)

IS_FLASK_APP = os.getenv("IS_FLASK_APP")
IS_FLASK_APP = bool(IS_FLASK_APP) if IS_FLASK_APP else False

BaseSession = None
if IS_FLASK_APP:
    from flask import _app_ctx_stack
    BaseSession = Session(_app_ctx_stack.__ident_func__)
else:
    BaseSession = Session()


def WithSession(BaseSession):
    @contextmanager
    def wrapper():
        session = BaseSession()
        try:
            yield session
        finally:
            #pass
            #session.rollback()
            #session.remove()
            session.expunge_all()
            BaseSession.remove()
    return wrapper

DBSession = WithSession(BaseSession)
DBEntity.query = BaseSession.query_property()

def create_tables():
    DBEntity.metadata.create_all(engine)
