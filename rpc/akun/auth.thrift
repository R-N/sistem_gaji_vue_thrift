
namespace py rpc.gen.akun.auth
namespace js rpc.gen.akun.auth


enum TUserRole{
	ADMIN_BIASA,
	ADMIN_UTAMA,
	ADMIN_AKUN,
	PENGAWAS,
	SUPER_ADMIN
}
const map<TUserRole, string> T_USER_ROLE_STR = {
	TUserRole.ADMIN_BIASA: "Admin Biasa",
	TUserRole.ADMIN_UTAMA: "Admin Utama",
	TUserRole.ADMIN_AKUN: "Admin Akun",
	TUserRole.PENGAWAS: "Pengawas",
	TUserRole.SUPER_ADMIN: "Super Admin"
}
const map<TUserRole, list<TUserRole>> T_USER_ROLE_DOUBLES = {
	TUserRole.ADMIN_BIASA: [TUserRole.ADMIN_BIASA, TUserRole.ADMIN_UTAMA, TUserRole.SUPER_ADMIN],
	TUserRole.ADMIN_UTAMA: [TUserRole.ADMIN_UTAMA, TUserRole.SUPER_ADMIN],
	TUserRole.ADMIN_AKUN: [TUserRole.ADMIN_AKUN, TUserRole.SUPER_ADMIN],
	TUserRole.PENGAWAS: [TUserRole.ADMIN_UTAMA, TUserRole.PENGAWAS, TUserRole.SUPER_ADMIN],
	TUserRole.SUPER_ADMIN: [TUserRole.SUPER_ADMIN]
}

struct TLoginResult {
    1: required string auth_token;
    2: optional string refresh_token;
}


enum TLoginErrorCode{
	USERNAME_KOSONG,
	PASSWORD_KOSONG,
	USERNAME_PASSWORD_SALAH,
	REFRESH_TOKEN_INVALID,
	REFRESH_TOKEN_EXPIRED,
	ALREADY_LOGGED_IN
}
const map<TLoginErrorCode, string> T_LOGIN_ERROR_STR = {
	TLoginErrorCode.USERNAME_KOSONG: "Username tidak boleh kosong",
	TLoginErrorCode.PASSWORD_KOSONG: "Password tidak boleh kosong",
	TLoginErrorCode.USERNAME_PASSWORD_SALAH: "Username atau password salah",
	TLoginErrorCode.REFRESH_TOKEN_INVALID: "Sesi invalid",
	TLoginErrorCode.REFRESH_TOKEN_EXPIRED: "Sesi kadaluarsa",
	TLoginErrorCode.ALREADY_LOGGED_IN: "Anda sudah login"
}
exception TLoginError{
	1: TLoginErrorCode code;
}

enum TAuthErrorCode{
	NOT_LOGGED_IN,
	AUTH_TOKEN_INVALID,
	AUTH_TOKEN_EXPIRED,
	INVALID_ROLE,
	NO_PERMISSION
}
const map<TAuthErrorCode, string> T_AUTH_ERROR_STR = {
	TAuthErrorCode.NOT_LOGGED_IN: "Username tidak boleh kosong",
	TAuthErrorCode.AUTH_TOKEN_INVALID: "Sesi invalid",
	TAuthErrorCode.AUTH_TOKEN_EXPIRED: "Sesi kadaluarsa",
	TAuthErrorCode.INVALID_ROLE: "Anda tidak berhak melakukan ini",
	TAuthErrorCode.NO_PERMISSION: "Anda tidak berhak melakukan ini"
}
exception TAuthError{
	1: TAuthErrorCode code;
}

service TAuthService
{
	TLoginResult login(
		1: string username, 
		2: string password
	) throws (
		1: TLoginError loginError
	);

	string refresh_auth(
		1: string auth_token,
		2: string refresh_token
	) throws (
		1: TAuthError authError,
		2: TLoginError loginError
	);
}