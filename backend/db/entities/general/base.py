from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DbGeneralEntity = declarative_base(metadata=MetaData(schema="general"))