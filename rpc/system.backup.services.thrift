include "user.auth.errors.thrift"
include "file.file.errors.thrift"
include "file.download.errors.thrift"
include "file.upload.errors.thrift"
include "system.backup.structs.thrift"

namespace py system.backup.services
namespace js system.backup.services

service TSystemBackupService{
	list<system.backup.structs.TBackupFile> fetch_backups(
		1: string auth_token
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	system.backup.structs.TBackupFile create_backup(
		1: string auth_token,
		2: string name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: file.file.errors.TFileError file_error
	);

	void delete_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: file.file.errors.TFileError file_error
	);

	string get_download_token(
		1: string auth_token,
		2: string file_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: file.file.errors.TFileError file_error,
		3: file.download.errors.TDownloadError download_error
	);

	string get_upload_token(
		1: string auth_token,
		2: string file_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: file.file.errors.TFileError file_error,
		3: file.upload.errors.TUploadError upload_error
	);

	void restore_backup(
		1: string auth_token,
		2: string file_name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: file.file.errors.TFileError file_error
	);
}