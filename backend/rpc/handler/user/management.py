from rpc.gen.user.management.services import TUserManagementService
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.user.structs.ttypes import TUser
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode

from models import models

class TUserManagementServiceHandler(TUserManagementService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']
        self.email_model = models['email']

    def fetch_akun(self, auth_token, query=None):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_users = self.user_model.fetch(query)
        return [u.fill(TUser()) for u in db_users]

    def register_akun(self, auth_token, form):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.register(auth_payload['role'], form)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.email_model.send_welcome(db_user)
        self.user_model.commit()
        user = db_user.fill(TUser())
        return user

    def set_role(self, auth_token, user_id, new_role):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.auth_model.require_role(auth_payload, new_role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION_SET_ROLE)
        self.user_model.set_role(auth_payload['role'], db_user, new_role)
        self.user_model.commit()


    def set_email(self, auth_token, user_id, new_email):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.user_model.set_email(auth_payload['role'], db_user, new_email)
        self.user_model.commit()

    def set_password(self, auth_token, user_id, new_password):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.SUPER_ADMIN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.user_model.set_password(auth_payload['role'], db_user, new_password)
        self.user_model.commit()

    def set_enabled(self, auth_token, user_id, new_enabled):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.user_model.set_enabled(auth_payload['role'], db_user, new_enabled)
        self.user_model.commit()

    def set_verified(self, auth_token, user_id, new_verified):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.SUPER_ADMIN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.user_model.set_verified(auth_payload['role'], db_user, new_verified)
        self.user_model.commit()

    def delete(self, auth_token, user_id):
        auth_payload = self.auth_model.require_role(auth_token, TUserRole.SUPER_ADMIN)
        db_user = self.user_model.get_by_id(user_id)
        self.auth_model.require_role(auth_payload, db_user.role, Exception=TUserManagementError, error_code=TUserManagementErrorCode.INSUFFICIENT_PERMISSION)
        self.user_model.delete(auth_payload['role'], db_user)
        self.user_model.commit()
