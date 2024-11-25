from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

DbCommitedEntity = declarative_base(metadata=MetaData(schema=os.getenv("DB_COMMITED", "sistem_gaji_commited")))