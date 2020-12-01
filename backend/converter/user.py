
from db.entities.general import DbUser as DB
from rpc.gen.user.user.structs.ttypes import TUser as RPC

# FK has to be deferrable

def db_to_rpc(db):
    return RPC(
        id=db.id,
        username=db.username,
        role=db.role,
        name=db.name,
        email=db.email,
        enabled=db.enabled,
        verified=db.verified
    )