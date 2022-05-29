namespace py data.departemen.errors
namespace js data.departemen.errors

enum TDepartemenErrorCode{
	NAMA_EMPTY,
	NAMA_INVALID,
	NAMA_TOO_LONG,
	NAMA_ALREADY_EXISTS,
	DEPARTEMEN_NOT_FOUND
}

const i32 NAMA_LEN_MAX = 50;

const string NAMA_REGEX_STR = "^[a-zA-Z0-9 \\.\\,\\&]+$";

const map<TDepartemenErrorCode, string> T_DEPARTEMEN_ERROR_STR = {
	TDepartemenErrorCode.NAMA_EMPTY: "Nama departemen tidak boleh kosong",
	TDepartemenErrorCode.NAMA_INVALID: "Nama departemen tidak valid. Nama departemen hanya boleh berisi huruf, angka, spasi, titik, koma, dan &.",
	TDepartemenErrorCode.NAMA_TOO_LONG: "Nama departemen terlalu panjang. Nama maksimal 50 karakter.",
	TDepartemenErrorCode.NAMA_ALREADY_EXISTS: "Nama departemen sudah digunakan.",
	TDepartemenErrorCode.DEPARTEMEN_NOT_FOUND: "Departemen tidak ditemukan.",
};

exception TDepartemenError{
	1: TDepartemenErrorCode code;
}