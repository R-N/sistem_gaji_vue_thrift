namespace js email.errors
namespace py email.errors

enum TEmailErrorCode{
	EMAIL_TOKEN_INVALID,
	EMAIL_TOKEN_EXPIRED,
	EMAIL_INVALID,
	EMAIL_NOT_FOUND,
	EMAIL_NOT_SENT
}
const map<TEmailErrorCode, string> T_EMAIL_ERROR_STR = {
	TEmailErrorCode.EMAIL_TOKEN_INVALID: "Email token invalid",
	TEmailErrorCode.EMAIL_TOKEN_EXPIRED: "Email token kadaluarsa",
	TEmailErrorCode.EMAIL_INVALID: "Email invalid",
	TEmailErrorCode.EMAIL_NOT_FOUND: "Email tidak ditemukan",
	TEmailErrorCode.EMAIL_NOT_SENT: "Gagal mengirim email"
}
exception TEmailError{
	1: TEmailErrorCode code;
}
