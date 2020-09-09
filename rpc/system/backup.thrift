include "../akun/auth.thrift"

namespace py rpc.gen.system.backup
namespace js rpc.gen.system.backup


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

service TBackupService{
	list<string> fetch_backups(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);

	void create_backup(
		1: string auth_token,
		2: string name
	) throws (
		1: auth.TAuthError authError,
		2: TFileError fileError
	);

	void delete_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: TFileError fileError
	);

	string download_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: TFileError fileError
	);

	string get_upload_token(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);
}