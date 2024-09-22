from rpc.gen.data.departemen.services import TDataDepartemenService
from rpc.gen.data.departemen.structs.ttypes import TDepartemen

from rpc.gen.user.user.types.ttypes import TUserRole
from ..crud import TCrudServiceHandler

from models import models

class TDataDepartemenServiceHandler(TDataDepartemenService.Iface, TCrudServiceHandler):
    def __init__(self):
        TDataDepartemenService.Iface.__init__(self)
        TCrudServiceHandler.__init__(
            self,
            "departemen", 
            TDepartemen,
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
            require_role=False
        )

