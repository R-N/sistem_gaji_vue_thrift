include "../akun/auth.thrift"
include "../file/file.thrift"
include "../file/download.thrift"
include "../file/upload.thrift"

namespace py rpc.gen.system.backup
namespace js rpc.gen.system.backup

struct TBackupFile {
	1: string file_name,
	2: string last_modified
}

service TBackupService{
	list<TBackupFile> fetch_backups(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);

	TBackupFile create_backup(
		1: string auth_token,
		2: string name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError
	);

	void delete_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError
	);

	string get_download_token(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError,
		3: download.TDownloadError downloadError
	);

	string get_upload_token(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError,
		3: upload.TUploadError uploadError
	);
}