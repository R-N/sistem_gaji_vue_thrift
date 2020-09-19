namespace py user.auth.errors
namespace js user.auth.errors

enum TLoginErrorCode{
	USERNAME_EMPTY,
	PASSWORD_EMPTY,
	USERNAME_PASSWORD_SALAH,
	PASSWORD_SALAH,
	REFRESH_TOKEN_INVALID,
	REFRESH_TOKEN_EXPIRED,
	ALREADY_LOGGED_IN,
	EMAIL_NOT_FOUND,
	USER_DISABLED,
	USER_UNVERIFIED
}
const map<TLoginErrorCode, string> T_LOGIN_ERROR_STR = {
	TLoginErrorCode.USERNAME_EMPTY: "Username tidak boleh kosong",
	TLoginErrorCode.PASSWORD_EMPTY: "Password tidak boleh kosong",
	TLoginErrorCode.USERNAME_PASSWORD_SALAH: "Username atau password salah",
	TLoginErrorCode.PASSWORD_SALAH: "Password salah",
	TLoginErrorCode.REFRESH_TOKEN_INVALID: "Sesi invalid",
	TLoginErrorCode.REFRESH_TOKEN_EXPIRED: "Sesi kadaluarsa",
	TLoginErrorCode.ALREADY_LOGGED_IN: "Anda sudah login",
	TLoginErrorCode.USER_DISABLED: "Akun Anda tidak aktif. Silahkan hubungi admin",
	TLoginErrorCode.USER_UNVERIFIED: "Akun Anda belum terverifikasi. Silahkan cek email Anda"
}
exception TLoginError{
	1: TLoginErrorCode code;
}

enum TAuthErrorCode{
	NOT_LOGGED_IN,
	AUTH_TOKEN_INVALID,
	AUTH_TOKEN_EXPIRED,
	ROLE_INVALID,
	NO_PERMISSION
}
const map<TAuthErrorCode, string> T_AUTH_ERROR_STR = {
	TAuthErrorCode.NOT_LOGGED_IN: "Username tidak boleh kosong",
	TAuthErrorCode.AUTH_TOKEN_INVALID: "Sesi invalid",
	TAuthErrorCode.AUTH_TOKEN_EXPIRED: "Sesi kadaluarsa",
	TAuthErrorCode.ROLE_INVALID: "Anda tidak berhak melakukan ini",
	TAuthErrorCode.NO_PERMISSION: "Anda tidak berhak melakukan ini"
}
exception TAuthError{
	1: TAuthErrorCode code;
}
