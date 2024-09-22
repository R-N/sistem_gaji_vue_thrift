namespace py data.job_level.errors
namespace js data.job_level.errors

enum TJobLevelErrorCode{
	ZERO,
	NAME_EMPTY,
	NAME_INVALID,
	NAME_TOO_LONG,
	NAME_ALREADY_EXISTS,
	JOB_LEVEL_NOT_FOUND,
    GAJI_POKOK_INVALID,
    TUNJANGAN_JABATAN_INVALID,
    UPAH_LEMBUR_INVALID,
    UPAH_LEMBUR_INVALID_2,
    UPAH_LEMBUR_1_INVALID,
    UPAH_LEMBUR_2_INVALID,
    UPAH_LEMBUR_3_INVALID,
}

const i32 NAME_MAX_LEN = 50;
const i32 MONEY_MAX_LEN = 13;

const string NAME_REGEX_STR = "^[a-zA-Z0-9 \\.\\,\\&]+$";

const map<TJobLevelErrorCode, string> T_JOB_LEVEL_ERROR_STR = {
	TJobLevelErrorCode.NAME_EMPTY: "Nama job level tidak boleh kosong",
	TJobLevelErrorCode.NAME_INVALID: "Nama job level tidak valid. Name job level hanya boleh berisi huruf, angka, spasi, titik, koma, dan &.",
	TJobLevelErrorCode.NAME_TOO_LONG: "Nama job level terlalu panjang. Name maksimal 50 karakter.",
	TJobLevelErrorCode.NAME_ALREADY_EXISTS: "Nama job level sudah digunakan.",
	TJobLevelErrorCode.JOB_LEVEL_NOT_FOUND: "Job level tidak ditemukan.",
	TJobLevelErrorCode.GAJI_POKOK_INVALID: "Gaji pokok tidak valid. Gaji pokok harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.TUNJANGAN_JABATAN_INVALID: "Tunjangan jabatan tidak valid. Tunjangan jabatan harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.UPAH_LEMBUR_INVALID: "Upah lembur tidak valid. Upah lembur harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.UPAH_LEMBUR_INVALID_2: "Upah lembur %s tidak valid. Upah lembur harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.UPAH_LEMBUR_1_INVALID: "Upah lembur 1 tidak valid. Upah lembur 1 harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.UPAH_LEMBUR_2_INVALID: "Upah lembur 2 tidak valid. Upah lembur 2 harus berupa bilangan bulat non-negatif.",
	TJobLevelErrorCode.UPAH_LEMBUR_3_INVALID: "Upah lembur 3 tidak valid. Upah lembur 3 harus berupa bilangan bulat non-negatif.",
};

exception TJobLevelError{
	1: TJobLevelErrorCode code;
}