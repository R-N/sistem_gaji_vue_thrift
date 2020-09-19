include "user.auth.errors.thrift"
include "user.user.errors.thrift"
include "user.email.errors.thrift"
include "email.errors.thrift"

namespace js user.email.services
namespace py user.email.services

service TUserEmailService {
	bool has_password(
		1: string token
	) throws (
		1: email.errors.TEmailError email_error,
		2: user.email.errors.TUserEmailError user_email_error,
		3: user.user.errors.TUserError user_error
	)
	void verify_email(
		1: string verify_token, 
		2: string password
	) throws (
		1: email.errors.TEmailError email_error,
		2: user.email.errors.TUserEmailError user_email_error,
		3: user.user.errors.TUserError user_error
	);

	void change_email(
		1: string verify_token,
		2: string password
	) throws (
		1: email.errors.TEmailError email_error,
		2: user.email.errors.TUserEmailError user_email_error,
		3: user.auth.errors.TLoginError login_error,
		4: user.user.errors.TUserError user_error
	);

	void set_password(
		1: string password_token,
		2: string password
	) throws (
		1: email.errors.TEmailError email_error,
		2: user.email.errors.TUserEmailError user_email_error,
		3: user.user.errors.TUserError user_error
	);
}