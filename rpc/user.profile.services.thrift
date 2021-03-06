include "user.auth.errors.thrift"
include "user.auth.structs.thrift"
include "user.user.errors.thrift"
include "user.user.structs.thrift"
include "user.email.errors.thrift"
include "email.errors.thrift"

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
		2: user.user.errors.TUserError user_error,
		3: email.errors.TEmailError email_error,
		4: user.email.errors.TUserEmailError user_email_error
	);

	user.auth.structs.TLoginResult set_password(
		1: string auth_token,
		2: string old_password,
		3: string new_password
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.auth.errors.TLoginError login_error,
		3: user.user.errors.TUserError user_error,
		4: email.errors.TEmailError email_error,
		5: user.email.errors.TUserEmailError user_email_error
	);

	void set_name(
		1: string auth_token,
		2: string new_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.user.errors.TUserError user_error
	);
}