namespace py rpc.gen.file.file
namespace js rpc.gen.file.file

enum TFileErrorCode{
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