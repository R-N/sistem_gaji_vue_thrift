include "user.auth.errors.thrift"
include "user.user.errors.thrift"
include "user.email.errors.thrift"


namespace py user.recovery.services
namespace js user.recovery.services

service TUserRecoveryService{
	void reset_password(
		1: string username
	) throws (
		1: user.auth.errors.TLoginError login_error,
		2: user.user.errors.TUserError user_error,
		3: user.email.errors.TEmailError email_error
	);

	void resend_verification(
		1: string username
	) throws (
		1: user.auth.errors.TLoginError login_error,
		2: user.user.errors.TUserError user_error,
		3: user.email.errors.TEmailError email_error
	);
}