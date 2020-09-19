namespace py user.user.errors
namespace js user.user.errors

enum TUserErrorCode{
	USERNAME_EMPTY,
	PASSWORD_EMPTY,
	NAME_EMPTY,
	EMAIL_EMPTY,
	ROLE_EMPTY,
	STATUS_EMPTY,
	USERNAME_INVALID,
	PASSWORD_INVALID,
	NAME_INVALID,
	EMAIL_INVALID,
	ROLE_INVALID,
	STATUS_INVALID,
	USERNAME_TOO_LONG,
	PASSWORD_TOO_LONG,
	NAME_TOO_LONG,
	EMAIL_TOO_LONG,
	PASSWORD_TOO_SHORT,
	USERNAME_ALREADY_EXISTS,
	EMAIL_ALREADY_EXISTS,
	USER_NOT_FOUND,
	USER_UNVERIFIED,
	USER_ALREADY_VERIFIED
}

const i32 USERNAME_LEN_MAX = 50;
const i32 NAME_LEN_MAX = 50;
const i32 PASSWORD_LEN_MIN = 8;
const i32 PASSWORD_LEN_MAX = 20;
const i32 EMAIL_LEN_MAX = 50;

const map<TUserErrorCode, string> T_USER_ERROR_STR = {
	TUserErrorCode.USERNAME_EMPTY: "Username tidak boleh kosong",
	TUserErrorCode.PASSWORD_EMPTY: "Password tidak boleh kosong",
	TUserErrorCode.NAME_EMPTY: "Nama tidak boleh kosong",
	TUserErrorCode.EMAIL_EMPTY: "Email tidak boleh kosong",
	TUserErrorCode.ROLE_EMPTY: "Role harus dipilih",
	TUserErrorCode.STATUS_EMPTY: "Status harus dipilih",
	TUserErrorCode.USERNAME_INVALID: "Username tidak valid",
	TUserErrorCode.PASSWORD_INVALID: "Password tidak valid. Password harus terdiri dari huruf kecil, huruf besar, angka, dan simbol.",
	TUserErrorCode.NAME_INVALID: "Nama tidak valid",
	TUserErrorCode.EMAIL_INVALID: "Email tidak valid",
	TUserErrorCode.ROLE_INVALID: "Role tidak valid",
	TUserErrorCode.STATUS_INVALID: "Status tidak valid",
	TUserErrorCode.USERNAME_TOO_LONG: "Username terlalu panjang. Username maksimal 50 karakter",
	TUserErrorCode.PASSWORD_TOO_LONG: "Password terlalu panjang. Password maksimal 20 karakter",
	TUserErrorCode.NAME_TOO_LONG: "Nama terlalu panjang. Nama maksimal 50 karakter.",
	TUserErrorCode.EMAIL_TOO_LONG: "Email terlalu panjang. Email maksimal 50 karakter.",
	TUserErrorCode.PASSWORD_TOO_SHORT: "Password terlalu pendek. Password minimal 8 karakter",
	TUserErrorCode.USERNAME_ALREADY_EXISTS: "Username sudah digunakan",
	TUserErrorCode.EMAIL_ALREADY_EXISTS: "Email sudah digunakan",
	TUserErrorCode.USER_NOT_FOUND: "User tidak ditemukan",
	TUserErrorCode.USER_UNVERIFIED: "Akun belum terverifikasi",
	TUserErrorCode.USER_ALREADY_VERIFIED: "Akun telah terverifikasi"
};

exception TUserError{
	1: TUserErrorCode code;
}