
from db.entities.staging import DbPerusahaan as Staging
from rpc.gen.data.perusahaan.structs.ttypes import TPerusahaan as RPC

# FK has to be deferrable

def staging_to_rpc(staging):
    return RPC(
        id=staging.id,
        nama=staging.nama,
        enabled=staging.enabled
    )