namespace js user.email.errors
namespace py user.email.errors

enum TUserEmailErrorCode{
	ZERO,
	RESET_PASSWORD_TOKEN_INVALID,
	RESET_PASSWORD_TOKEN_EXPIRED,
	EMAIL_VERIFICATION_TOKEN_INVALID,
	EMAIL_VERIFICATION_TOKEN_EXPIRED,
	EMAIL_CHANGE_TOKEN_INVALID,
	EMAIL_CHANGE_TOKEN_EXPIRED
}
const map<TUserEmailErrorCode, string> T_USER_EMAIL_ERROR_STR = {
	TUserEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID: "Token reset password invalid",
	TUserEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED: "Token reset password kadaluarsa",
	TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID: "Token verifikasi email invalid",
	TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED: "Token verifikasi email kadaluarsa",
	TUserEmailErrorCode.EMAIL_CHANGE_TOKEN_INVALID: "Token ganti email invalid",
	TUserEmailErrorCode.EMAIL_CHANGE_TOKEN_EXPIRED: "Token ganti email kadaluarsa"
}
exception TUserEmailError{
	1: TUserEmailErrorCode code;
}
