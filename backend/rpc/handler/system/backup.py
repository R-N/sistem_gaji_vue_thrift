from flask import request

from rpc.gen.system.backup.services import TSystemBackupService
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.system.backup.structs.ttypes import TBackupFile

import db
from models import models

class TSystemBackupServiceHandler(TSystemBackupService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.backup_model = models['backup']

    def create_backup(self, auth_token, name):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        file_name, last_modified = self.backup_model.create_backup(name)
        return TBackupFile(file_name, last_modified)

    def fetch_backups(self, auth_token):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        files = self.backup_model.fetch_backups()
        return [TBackupFile(file_name, last_modified) for file_name, last_modified in files]

    def get_download_token(self, auth_token, file_name):
        ip = request.remote_addr
        return self.backup_model.create_download_token(ip, file_name)

    def get_upload_token(self, auth_token, file_name):
        ip = request.remote_addr
        return self.backup_model.create_upload_token(ip, file_name)

    def delete_backup(self, auth_token, file_name):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        return self.backup_model.delete_backup(file_name)

    def restore_backup(self, auth_token, file_name):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.SUPER_ADMIN)
        self.backup_model.restore_backup(file_name)
        db.commit()