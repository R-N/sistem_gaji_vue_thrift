from rpc.gen.user.management.services import TUserManagementService
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.user.structs.ttypes import TUser
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode
from ..crud import TCrudServiceHandler

from models import models

class TUserManagementServiceHandler(TUserManagementService.Iface, TCrudServiceHandler):
    def __init__(self):
        TUserManagementService.Iface.__init__(self)
        TCrudServiceHandler.__init__(
            self,
            "user", 
            TUser,
            actions={
                "fetch": TUserRole.ADMIN_AKUN,
                "delete": TUserRole.ADMIN_AKUN,
            },
            setters={
                "name": TUserRole.SUPER_ADMIN,
                "role": TUserRole.ADMIN_AKUN,
                "email": TUserRole.SUPER_ADMIN,
                "password": TUserRole.SUPER_ADMIN,
                "enabled": TUserRole.ADMIN_AKUN,
                "verified": TUserRole.SUPER_ADMIN,
            },
            require_role=True
        )
        self.email_model = models['email']

    # def set_email(self, auth_token, id, email):
    #     raise NotImplementedError()

    def create(self, auth_token, form):
        actor = self.auth_model.require_role(auth_token, TUserRole.ADMIN_AKUN)
        db_user = self.model.create(form, actor=actor)
        self.email_model.send_welcome(db_user)
        self.model.commit()
        user = db_user.fill(TUser())
        return user
