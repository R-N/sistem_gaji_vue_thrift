from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DbLaporanEntity = declarative_base(metadata=MetaData(schema="laporan"))