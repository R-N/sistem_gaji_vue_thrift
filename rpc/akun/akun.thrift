include "../akun/auth.thrift"
include "../akun/user.thrift"

namespace py rpc.gen.akun.akun
namespace js rpc.gen.akun.akun

struct TUserForm{
	1: string username;
	2: optional string password;
	3: string name;
	4: string email;
	5: auth.TUserRole role;
}


struct TAkunQuery{
	1: optional i32 limit;
	2: optional i32 offset;
	3: optional bool verified;
	4: optional bool enabled;
	5: optional auth.TUserRole role;
}

service TAkunService{
	list<user.TUser> fetch_akun(
		1: string auth_token,
		2: TAkunQuery query
	) throws (
		1: auth.TAuthError auth_error
	);

	user.TUser register_akun(
		1: string auth_token,
		2: TUserForm form
	) throws (
		1: auth.TAuthError auth_error,
		2: user.TUserError user_error
	);

	void set_role(
		1: string auth_token,
		2: i32 user_id,
		3: auth.TUserRole new_role
	) throws (
		1: auth.TAuthError auth_error,
		2: user.TUserError user_error
	);

	void set_email(
		1: string auth_token,
		2: i32 user_id,
		3: string new_email
	) throws (
		1: auth.TAuthError auth_error,
		2: user.TUserError user_error
	);

	void set_password(
		1: string auth_token,
		2: i32 user_id,
		3: string new_password
	) throws (
		1: auth.TAuthError auth_error,
		2: user.TUserError user_error
	);

	void set_enabled(
		1: string auth_token,
		2: i32 user_id,
		3: bool new_enabled
	) throws (
		1: auth.TAuthError auth_error,
		2: user.TUserError user_error
	);
}