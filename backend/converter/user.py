
from db.entities import DBUser
from rpc.gen.user.user.structs.ttypes import TUser

def DBUser_TUser(db_user):
	return TUser(
		id=db_user.id,
		username=db_user.username,
		role=db_user.role,
		name=db_user.name,
		email=db_user.email,
		enabled=db_user.enabled,
		verified=db_user.verified
	)