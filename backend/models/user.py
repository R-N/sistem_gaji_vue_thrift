from rpc.gen.akun.ttypes import User, UserRole
users = {
    'admin': User('Admin Biasa', UserRole.ADMIN_BIASA),
    'admin_utama': User('Admin Utama', UserRole.ADMIN_UTAMA)
}

class UserModel:
    def __init__(self):
        pass

    def get_user(self, username):
        if username not in users:
            return None
        return users[username]
