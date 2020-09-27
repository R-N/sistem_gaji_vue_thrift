from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DbStagingEntity = declarative_base(metadata=MetaData(schema="staging"))