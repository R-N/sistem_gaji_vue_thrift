include "../akun/auth.thrift"
include "../file/file.thrift"

namespace py rpc.gen.system.backup
namespace js rpc.gen.system.backup

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
		2: file.TFileError fileError
	);

	void delete_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError
	);

	string download_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: auth.TAuthError authError,
		2: file.TFileError fileError
	);

	string get_upload_token(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);
}