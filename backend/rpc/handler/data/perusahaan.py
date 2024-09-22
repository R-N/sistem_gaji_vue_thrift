from rpc.gen.data.perusahaan.services import TDataPerusahaanService
from rpc.gen.data.perusahaan.structs.ttypes import TPerusahaan

from rpc.gen.user.user.types.ttypes import TUserRole
from ..crud import TCrudServiceHandler

from models import models

class TDataPerusahaanServiceHandler(TDataPerusahaanService.Iface, TCrudServiceHandler):
    def __init__(self):
        TDataPerusahaanService.Iface.__init__(self)
        TCrudServiceHandler.__init__(
            self,
            "perusahaan", 
            TPerusahaan,
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

