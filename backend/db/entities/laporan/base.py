from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

DbLaporanEntity = declarative_base(metadata=MetaData(schema=os.getenv("DB_LAPORAN", "sistem_gaji_laporan")))