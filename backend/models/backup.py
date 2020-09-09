from pyexcel_io import get_data
from pyexcel_io.constants import DB_SQL
from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter
from rpc.gen.file.file.ttypes import TFileError, TFileErrorCode
from db import DBSession
from db.entities import DBUser
from datetime import date
from pyexcel_xlsx import save_data as save_to_xlsx
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from .manager import get_model
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

BACKUP_TABLES = [DBUser]
BACKUP_PATH = "backups"

class BackupModel:
    def __init__(self):
        pass

    def create_backup(self, name):
        file_name = "%s %s.xlsx" % (str(date.today()), name)
        file_path = "%s/%s" % (BACKUP_PATH, file_name)
        file = Path(file_path)
        if file.exists():
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)
        with DBSession() as session:
            exporter = SQLTableExporter(session)
            for table in BACKUP_TABLES:
                adapter = SQLTableExportAdapter(table)
                exporter.append(adapter)
            data = get_data(exporter, file_type=DB_SQL)
            #data['users2'] = data['users']
            save_to_xlsx(file_path, data)

    def fetch_backups(self):
        files = [f for f in listdir(BACKUP_PATH) if isfile(join(BACKUP_PATH, f))]
        return files

    def download_backup(self, ip, file_name):
        return get_model("download").download(ip, BACKUP_PATH, file_name)


