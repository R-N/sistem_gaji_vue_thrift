from rpc.gen.user.management.services import TUserManagementService
from rpc.gen.user.user.types.ttypes import TUserRole

from models import models
from converter.user import DbUser_TUser

class TUserManagementServiceHandler(TUserManagementService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']
        self.email_model = models['email']

    def fetch_akun(self, auth_token, query):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_users = self.user_model.fetch_users(query)
        return [DbUser_TUser(u) for u in db_users]

    def register_akun(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.register_user(auth_payload['role'], form)
        self.email_model.send_welcome(db_user)
        self.user_model.commit()
        return DbUser_TUser(db_user)

    def set_role(self, auth_token, user_id, new_role):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_user_by_id(user_id)
        self.user_model.set_role(auth_payload['role'], db_user, new_role)
        self.user_model.commit()


    def set_email(self, auth_token, user_id, new_email):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_user_by_id(user_id)
        self.user_model.set_email(auth_payload['role'], db_user, new_email)
        self.user_model.commit()

    def set_password(self, auth_token, user_id, new_password):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.SUPER_ADMIN)
        db_user = self.user_model.get_user_by_id(user_id)
        self.user_model.set_password(auth_payload['role'], db_user, new_password)
        self.user_model.commit()

    def set_enabled(self, auth_token, user_id, new_enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_user_by_id(user_id)
        self.user_model.set_enabled(auth_payload['role'], db_user, new_enabled)
        self.user_model.commit()
