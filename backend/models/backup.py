from pyexcel_io import get_data
from pyexcel_io.constants import DB_SQL
from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter
from db import DBSession
from db.entities import DBUser
from datetime import date
from pyexcel_xlsx import save_data as save_to_xlsx
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

BACKUP_TABLES = [DBUser]

class BackupModel:
    def __init__(self):
        pass

    def create_backup(self, name):
        filename = "%s/%s %s.xlsx" % ("backups", str(date.today()), name)
        with DBSession() as session:
            exporter = SQLTableExporter(session)
            for table in BACKUP_TABLES:
                adapter = SQLTableExportAdapter(table)
                exporter.append(adapter)
            data = get_data(exporter, file_type=DB_SQL)
            #data['users2'] = data['users']
            save_to_xlsx(filename, data)
