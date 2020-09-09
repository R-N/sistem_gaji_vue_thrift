from rpc.gen.system.backup import TBackupService
from rpc.gen.akun.auth.ttypes import TUserRole
from models import get_model

class TBackupServiceHandler(TBackupService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.backup_model = get_model('backup')

    def create_backup(self, auth_token, name):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        self.backup_model.create_backup(name)

    def fetch_backups(self, auth_token):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_UTAMA)
        return self.backup_model.fetch_backups()
