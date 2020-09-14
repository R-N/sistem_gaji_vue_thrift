include "../akun/auth.thrift"

namespace py rpc.gen.akun.user
namespace js rpc.gen.akun.user

struct TUser{
	1: i32 id;
	2: string username;
	3: auth.TUserRole role;
	4: string name;
	5: string email;
	6: bool enabled;
}

enum TUserErrorCode{
	USERNAME_EMPTY,
	PASSWORD_EMPTY,
	NAME_EMPTY,
	EMAIL_EMPTY,
	ROLE_EMPTY,
	USERNAME_INVALID,
	PASSWORD_INVALID,
	NAME_INVALID,
	EMAIL_INVALID,
	ROLE_INVALID,
	USERNAME_ALREADY_EXISTS,
	EMAIL_ALREADY_EXISTS,
	USER_NOT_FOUND,
	EMAIL_NOT_FOUND
}
const map<TUserErrorCode, string> T_USER_ERROR_STR = {
	TUserErrorCode.USERNAME_EMPTY: "Username tidak boleh kosong",
	TUserErrorCode.PASSWORD_EMPTY: "Password tidak boleh kosong",
	TUserErrorCode.NAME_EMPTY: "Nama tidak boleh kosong",
	TUserErrorCode.EMAIL_EMPTY: "Email tidak boleh kosong",
	TUserErrorCode.ROLE_EMPTY: "Role harus dipilih",
	TUserErrorCode.USERNAME_INVALID: "Username tidak valid",
	TUserErrorCode.PASSWORD_INVALID: "Password tidak valid. Password harus sepanjang 8-20 karakter dan terdiri dari huruf kecil, huruf besar, angka, dan simbol.",
	TUserErrorCode.NAME_INVALID: "Nama tidak valid",
	TUserErrorCode.EMAIL_INVALID: "Email tidak valid",
	TUserErrorCode.ROLE_INVALID: "Role tidak valid",
	TUserErrorCode.USERNAME_ALREADY_EXISTS: "Username sudah digunakan",
	TUserErrorCode.EMAIL_ALREADY_EXISTS: "Email sudah digunakan",
	TUserErrorCode.USER_NOT_FOUND: "User tidak ditemukan",
	TUserErrorCode.EMAIL_NOT_FOUND: "Email tidak ditemukan"
}
exception TUserError{
	1: TUserErrorCode code;
}
service TUserService{
	TUser get_user(
		1: string auth_token
	) throws (
		1: auth.TAuthError auth_error
	);

	void set_email(
		1: string auth_token,
		2: string new_email
	) throws (
		1: auth.TAuthError auth_error,
		2: TUserError user_error
	);

	auth.TLoginResult set_password(
		1: string auth_token,
		2: string new_password
	) throws (
		1: auth.TAuthError auth_error,
		2: TUserError user_error
	);

	void set_name(
		1: string auth_token,
		2: string new_name
	) throws (
		1: auth.TAuthError auth_error,
		2: TUserError user_error
	);
}