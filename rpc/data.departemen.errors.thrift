namespace py data.departemen.errors
namespace js data.departemen.errors

enum TDepartemenErrorCode{
	ZERO,
	NAME_EMPTY,
	NAME_INVALID,
	NAME_TOO_LONG,
	NAME_ALREADY_EXISTS,
	DEPARTEMEN_NOT_FOUND,
	PERUSAHAAN_NOT_FOUND
}

const i32 NAME_MAX_LEN = 50;

const string NAME_REGEX_STR = "^[a-zA-Z0-9 \\.\\,\\&]+$";

const map<TDepartemenErrorCode, string> T_DEPARTEMEN_ERROR_STR = {
	TDepartemenErrorCode.NAME_EMPTY: "Nama departemen tidak boleh kosong",
	TDepartemenErrorCode.NAME_INVALID: "Nama departemen tidak valid. Nama departemen hanya boleh berisi huruf, angka, spasi, titik, koma, dan &.",
	TDepartemenErrorCode.NAME_TOO_LONG: "Nama departemen terlalu panjang. Name maksimal 50 karakter.",
	TDepartemenErrorCode.NAME_ALREADY_EXISTS: "Nama departemen sudah digunakan.",
	TDepartemenErrorCode.DEPARTEMEN_NOT_FOUND: "Departemen tidak ditemukan.",
	TDepartemenErrorCode.PERUSAHAAN_NOT_FOUND: "Perusahaan tidak ditemukan.",
};

exception TDepartemenError{
	1: TDepartemenErrorCode code;
}