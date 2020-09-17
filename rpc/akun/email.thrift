include "../akun/auth.thrift"
include "../akun/user.thrift"

namespace js rpc.gen.akun.email
namespace py rpc.gen.akun.email

enum TEmailErrorCode{
	EMAIL_TOKEN_INVALID,
	EMAIL_TOKEN_EXPIRED,
	RESET_PASSWORD_TOKEN_INVALID,
	RESET_PASSWORD_TOKEN_EXPIRED,
	EMAIL_VERIFICATION_TOKEN_INVALID,
	EMAIL_VERIFICATION_TOKEN_EXPIRED,
	EMAIL_CHANGE_TOKEN_INVALID,
	EMAIL_CHANGE_TOKEN_EXPIRED,
	EMAIL_INVALID,
	EMAIL_NOT_FOUND
}
const map<TEmailErrorCode, string> T_EMAIL_ERROR_STR = {
	TEmailErrorCode.EMAIL_TOKEN_INVALID: "Email token invalid",
	TEmailErrorCode.EMAIL_TOKEN_EXPIRED: "Email token kadaluarsa",
	TEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID: "Token reset password invalid",
	TEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED: "Token reset password kadaluarsa",
	TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID: "Token verifikasi email invalid",
	TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED: "Token verifikasi email kadaluarsa",
	TEmailErrorCode.EMAIL_CHANGE_TOKEN_INVALID: "Token ganti email invalid",
	TEmailErrorCode.EMAIL_CHANGE_TOKEN_EXPIRED: "Token ganti email kadaluarsa",
	TEmailErrorCode.EMAIL_INVALID: "Email invalid",
	TEmailErrorCode.EMAIL_NOT_FOUND: "Email tidak ditemukan"
}
exception TEmailError{
	1: TEmailErrorCode code;
}

service TEmailService {
	bool has_password(
		1: string token
	) throws (
		1: TEmailError token,
		2: user.TUserError user_error
	)
	void verify_email(
		1: string verify_token, 
		2: string password
	) throws (
		1: TEmailError email_error,
		2: user.TUserError user_error
	);

	void change_email(
		1: string verify_token,
		2: string password
	) throws (
		1: TEmailError email_error,
		2: auth.TLoginError login_error
	);

	void set_password(
		1: string password_token,
		2: string password
	) throws (
		1: TEmailError email_error,
		2: user.TUserError user_error
	);
}