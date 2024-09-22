from sqlalchemy.exc import IntegrityError

from rpc.gen.data.departemen.structs.ttypes import TDepartemenForm, TDepartemen
from rpc.gen.data.departemen.errors.ttypes import TDepartemenError, TDepartemenErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole

import db
from db.entities.staging import DbDepartemen
from db.errors import UniqueError
from .crud import CrudModel

class DepartemenModel(CrudModel):
    def __init__(self):
        CrudModel.__init__(
            self, 
            DbDepartemen, 
            TDepartemenError, 
            TDepartemenErrorCode,
            "DEPARTEMEN", 
            name_field="name", 
            actions={
                "get": TUserRole.ADMIN_BIASA,
                "create": TUserRole.ADMIN_UTAMA,
                "fetch": TUserRole.ADMIN_BIASA,
                "delete": TUserRole.SUPER_ADMIN,
            },
            setters={
                "name": TUserRole.ADMIN_UTAMA,
                "enabled": TUserRole.ADMIN_UTAMA,
            },
        )

