namespace py rpc.gen.akun
namespace js rpc.gen.akun

typedef i32 int
typedef i64 long

enum UserRole{
	ADMIN_BIASA,
	ADMIN_UTAMA,
	ADMIN_AKUN,
	PENGAWAS,
	SUPER_ADMIN
}
struct User{
	1: string name;
	2: UserRole role;
}
struct LoginResult {
    1: required string auth_token;
    2: optional string refresh_token;
}


enum LoginErrorCode{
	USERNAME_KOSONG,
	PASSWORD_KOSONG,
	USERNAME_PASSWORD_SALAH,
	REFRESH_TOKEN_INVALID,
	REFRESH_TOKEN_EXPIRED,
	ALREADY_LOGGED_IN
}
exception LoginError{
	1: LoginErrorCode code;
}

enum AuthErrorCode{
	NOT_LOGGED_IN,
	AUTH_TOKEN_INVALID,
	AUTH_TOKEN_EXPIRED,
	INVALID_ROLE,
	NO_PERMISSION
}
exception AuthError{
	1: AuthErrorCode code;
}

service AuthService
{
	LoginResult login(
		1: string username, 
		2: string password
	) throws (
		1: LoginError loginError
	);

	string refresh_auth(
		1: string auth_token,
		2: string refresh_token
	) throws (
		1: AuthError authError,
		2: LoginError loginError
	);

	User get_user(
		1: string auth_token
	) throws (
		1: AuthError authError
	);
}