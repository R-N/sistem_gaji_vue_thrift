namespace py file.file.errors
namespace js file.file.errors

const string FILE_NAME_REGEX_STR = "^(?!\\.)(?!com[0-9]$)(?!con$)(?!lpt[0-9]$)(?!nul$)(?!prn$)[^\\|*\\?\\\\:<>/$\"]*[^\\.\\|*\\?\\\\:<>/$\"]+$";

enum TFileErrorCode{
	ZERO,
	FILE_NOT_FOUND,
	FILE_ALREADY_EXISTS,
	FILE_NAME_EMPTY,
	FILE_NAME_INVALID
}
const map<TFileErrorCode, string> T_FILE_ERROR_STR = {
	TFileErrorCode.FILE_NOT_FOUND: "File tidak ditemukan",
	TFileErrorCode.FILE_ALREADY_EXISTS: "File sudah ada",
	TFileErrorCode.FILE_NAME_EMPTY: "Nama file tidak boleh kosong",
	TFileErrorCode.FILE_NAME_INVALID: "Nama file tidak valid"
}
exception TFileError{
	1: TFileErrorCode code;
}
