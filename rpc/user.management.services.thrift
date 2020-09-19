include "user.auth.errors.thrift"
include "user.user.types.thrift"
include "user.user.errors.thrift"
include "user.user.structs.thrift"
include "user.management.structs.thrift"

namespace py user.management.services
namespace js user.management.services

service TUserManagementService{
	list<user.user.structs.TUser> fetch_akun(
		1: string auth_token,
		2: user.management.structs.TUserQuery query
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	user.user.structs.TUser register_akun(
		1: string auth_token,
		2: user.management.structs.TUserRegistrationForm form
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	void set_role(
		1: string auth_token,
		2: i32 user_id,
		3: user.user.types.TUserRole new_role
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	void set_email(
		1: string auth_token,
		2: i32 user_id,
		3: string new_email
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	void set_password(
		1: string auth_token,
		2: i32 user_id,
		3: string new_password
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	void set_enabled(
		1: string auth_token,
		2: i32 user_id,
		3: bool new_enabled
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);
}