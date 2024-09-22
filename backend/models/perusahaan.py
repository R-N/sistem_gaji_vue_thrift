from sqlalchemy.exc import IntegrityError

from rpc.gen.data.perusahaan.structs.ttypes import TPerusahaanForm, TPerusahaan
from rpc.gen.data.perusahaan.errors.ttypes import TPerusahaanError, TPerusahaanErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole

import db
from db.entities.staging import DbPerusahaan
from db.errors import UniqueError
from .crud import CrudModel

class PerusahaanModel(CrudModel):
    def __init__(self):
        CrudModel.__init__(
            self, 
            DbPerusahaan, 
            TPerusahaanError, 
            TPerusahaanErrorCode,
            "PERUSAHAAN", 
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

