from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os
from dotenv import load_dotenv

from .session import make_session
from .scopefunc import get_scopefunc

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "sistem_gaji")

connect_str = "postgresql+psycopg2://%s:%s@%s:%s/%s"

connect_str_main = connect_str % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
engine_main = create_engine(connect_str_main)
# engine_staging = engine_main  # change this to move to separate db
engine = engine_main

# DbMainEntity = declarative_base(bind=engine_main)
# DbStagingEntity = declarative_base(bind=engine_staging)  # To separate them
# DbEntity = DbMainEntity

# connect_str_commited = connect_str % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_COMMITED)
# engine_commited = create_engine(connect_str_commited)

# DbCommitedEntity = declarative_base(bind=engine_commited)

SCOPEFUNC = get_scopefunc()

session_main = make_session(engine_main, scopefunc=SCOPEFUNC)
# session_staging = session_main  # change this to move to separate db
session = session_main

# session_commited = make_session(engine_commited, scopefunc=SCOPEFUNC)
