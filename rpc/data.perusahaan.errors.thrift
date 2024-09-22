namespace py data.perusahaan.errors
namespace js data.perusahaan.errors

enum TPerusahaanErrorCode{
	ZERO,
	NAME_EMPTY,
	NAME_INVALID,
	NAME_TOO_LONG,
	NAME_ALREADY_EXISTS,
	PERUSAHAAN_NOT_FOUND
}

const i32 NAME_MAX_LEN = 50;

const string NAME_REGEX_STR = "^[a-zA-Z0-9 \\.\\,\\&]+$";

const map<TPerusahaanErrorCode, string> T_PERUSAHAAN_ERROR_STR = {
	TPerusahaanErrorCode.NAME_EMPTY: "Nama perusahaan tidak boleh kosong",
	TPerusahaanErrorCode.NAME_INVALID: "Nama perusahaan tidak valid. Name perusahaan hanya boleh berisi huruf, angka, spasi, titik, koma, dan &.",
	TPerusahaanErrorCode.NAME_TOO_LONG: "Nama perusahaan terlalu panjang. Name maksimal 50 karakter.",
	TPerusahaanErrorCode.NAME_ALREADY_EXISTS: "Nama perusahaan sudah digunakan.",
	TPerusahaanErrorCode.PERUSAHAAN_NOT_FOUND: "Perusahaan tidak ditemukan.",
};

exception TPerusahaanError{
	1: TPerusahaanErrorCode code;
}