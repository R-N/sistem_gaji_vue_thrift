from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DbCommitedEntity = declarative_base(metadata=MetaData(schema="commited"))