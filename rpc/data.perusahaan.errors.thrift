namespace py data.perusahaan.errors
namespace js data.perusahaan.errors

enum TPerusahaanErrorCode{
	ZERO,
	NAMA_EMPTY,
	NAMA_INVALID,
	NAMA_TOO_LONG,
	NAMA_ALREADY_EXISTS,
	PERUSAHAAN_NOT_FOUND
}

const i32 NAMA_MAX_LEN = 50;

const string NAMA_REGEX_STR = "^[a-zA-Z0-9 \\.\\,\\&]+$";

const map<TPerusahaanErrorCode, string> T_PERUSAHAAN_ERROR_STR = {
	TPerusahaanErrorCode.NAMA_EMPTY: "Nama perusahaan tidak boleh kosong",
	TPerusahaanErrorCode.NAMA_INVALID: "Nama perusahaan tidak valid. Nama perusahaan hanya boleh berisi huruf, angka, spasi, titik, koma, dan &.",
	TPerusahaanErrorCode.NAMA_TOO_LONG: "Nama perusahaan terlalu panjang. Nama maksimal 50 karakter.",
	TPerusahaanErrorCode.NAMA_ALREADY_EXISTS: "Nama perusahaan sudah digunakan.",
	TPerusahaanErrorCode.PERUSAHAAN_NOT_FOUND: "Perusahaan tidak ditemukan.",
};

exception TPerusahaanError{
	1: TPerusahaanErrorCode code;
}