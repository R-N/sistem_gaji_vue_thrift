from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

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
engine = create_engine(connect_str, echo=True)

Base = declarative_base()