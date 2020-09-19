include "user.auth.errors.thrift"
include "user.auth.structs.thrift"
include "user.user.errors.thrift"
include "user.user.structs.thrift"

namespace py user.profile.services
namespace js user.profile.services

service TUserProfileService{
	user.user.structs.TUser get_user(
		1: string auth_token
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	void change_email(
		1: string auth_token,
		2: string new_email
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	user.auth.structs.TLoginResult set_password(
		1: string auth_token,
		2: string new_password
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);

	void set_name(
		1: string auth_token,
		2: string new_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);
}