from pyexcel_io import get_data
from pyexcel_io.constants import DB_SQL
from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter
from rpc.gen.file.file.ttypes import TFileError, TFileErrorCode
from rpc.gen.file.upload.ttypes import TUploadError, TUploadErrorCode
from db import DBSession
from db.entities import DBUser
from datetime import date
from pyexcel_xlsx import save_data as save_to_xlsx
from os import listdir
from os.path import isfile, join
from pathlib import Path
from .manager import get_model
from utils.file import file_exists, file_allowed
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
        file_path = self.make_file_path(file_name)
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
        files = [f for f in listdir(self.backup_path) if isfile(join(self.backup_path, f))]
        return files

    def make_file_path(self, file_name):
        return "%s/%s" % (self.backup_path, file_name)

    def create_download_token(self, ip, file_name):
        if not file_exists(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        return get_model("download").encode(ip, self.model_name, file_name)

    def create_upload_token(self, ip, file_name):
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        if file_exists(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)
        return get_model("upload").encode(ip, self.model_name, file_name)

    def decode_download_token(self, ip, token):
        payload = get_model("download").decode(ip, self.model_name, token)
        file_name = payload['name']
        if not file_exists(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_NOT_FOUND)
        return payload

    def decode_upload_token(self, ip, token):
        payload = get_model("upload").decode(ip, self.model_name, token)
        file_name = payload['name']
        if not file_allowed(file_name, self.allowed_extensions):
            raise TUploadError(TUploadErrorCode.FILE_INVALID)
        if file_exists(self.backup_path, file_name):
            raise TFileError(TFileErrorCode.FILE_ALREADY_EXISTS)
        return payload

