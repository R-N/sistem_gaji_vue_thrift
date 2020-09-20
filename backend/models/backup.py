from pyexcel_io import get_data as get_db_data, save_data as save_db_data
from pyexcel_io.constants import DB_SQL
from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter, SQLTableImporter, SQLTableImportAdapter
from datetime import date
from pyexcel_xlsx import save_data as save_to_xlsx, get_data as read_xlsx
from os import listdir
from os.path import isfile, join, getmtime
from pathlib import Path

from rpc.gen.file.file.errors.ttypes import TFileError, TFileErrorCode
from rpc.gen.file.upload.errors.ttypes import TUploadError, TUploadErrorCode

import db
from db.entities import DBUser
from utils.file import get_file, file_allowed, last_modified

from .manager import basic_models
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

BACKUP_TABLES = [DBUser]
BACKUP_PATH = "backups"
ALLOWED_EXTENSIONS = ["xlsx"]

class BackupModel:
    def __init__(self, backup_path=BACKUP_PATH, allowed_extensions=ALLOWED_EXTENSIONS):
        self.model_name = "backup"
        self.backup_path = backup_path
        self.allowed_extensions = allowed_extensions

    def create_backup(self, name):
        file_name = "%s %s.xlsx" % (str(date.today()), name)
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        if get_file(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)

        exporter = SQLTableExporter(db.session)
        for table in BACKUP_TABLES:
            adapter = SQLTableExportAdapter(table)
            exporter.append(adapter)
        data = get_db_data(exporter, file_type=DB_SQL)
        
        file_path = join(self.backup_path, file_name)
        save_to_xlsx(file_path, data)
        return file_name, str(last_modified(file_path))

    def restore_backup(self, file_name):
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        file_path = get_file(self.backup_path, file_name)
        if not file_path:
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        data = read_xlsx(str(file_path))
        # db.session.execute("SET session_replication_role = replica;")
        db.session.execute("SET CONSTRAINTS ALL DEFERRED")
        importer = SQLTableImporter(db.session)

        to_import = {}
        for table in BACKUP_TABLES:
            adapter = SQLTableImportAdapter(table)
            adapter.column_names = data[table.__tablename__][0]
            to_import[adapter.get_name()] = data[table.__tablename__][1:]
            importer.append(adapter)

        table_names = [table.__tablename__ for table in BACKUP_TABLES]
        db.session.execute("TRUNCATE %s RESTART IDENTITY" % (', '.join(table_names),))
        save_db_data(importer, to_import, file_type=DB_SQL)
        db.session.query(DBUser).update({
            DBUser.refresh_secret_2: None,
            DBUser.email_secret_2: None
        }, synchronize_session=False)
        # db.commit()

    def fetch_backups(self):
        files = [(f, str(last_modified(join(self.backup_path, f)))) for f in listdir(self.backup_path) if isfile(join(self.backup_path, f))]
        return files

    def make_file_path(self, file_name):
        return "%s/%s" % (self.backup_path, file_name)

    def create_download_token(self, ip, file_name):
        if not get_file(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        return basic_models["download"].encode(
            self.model_name,
            ip,
            {'file_name': file_name}
        )

    def create_upload_token(self, ip, file_name):
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        if get_file(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)
        return basic_models["upload"].encode(
            self.model_name,
            ip,
            {'file_name': file_name}
        )

    def decode_download_token(self, ip, token):
        payload = basic_models["download"].decode(self.model_name, ip, token)
        file_name = payload['file_name']
        if not get_file(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        return payload

    def decode_upload_token(self, ip, token):
        payload = basic_models["upload"].decode(self.model_name, ip, token)
        file_name = payload['file_name']
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        if get_file(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)
        return payload

    def delete_backup(self, file_name):
        file = get_file(self.backup_path, file_name)
        if not file:
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        file.unlink()
