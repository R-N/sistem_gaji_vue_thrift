namespace py rpc.gen.akun
namespace js rpc.gen.akun

typedef i32 int
typedef i64 long

enum TUserRole{
	ADMIN_BIASA,
	ADMIN_UTAMA,
	ADMIN_AKUN,
	PENGAWAS,
	SUPER_ADMIN
}
struct TUser{
	1: int id;
	2: string name;
	3: TUserRole role;
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

	TUser get_user(
		1: string auth_token
	) throws (
		1: TAuthError authError
	);
}