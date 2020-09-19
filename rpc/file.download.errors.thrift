namespace py file.download.errors
namespace js file.download.errors

enum TDownloadErrorCode{
	DOWNLOAD_TOKEN_INVALID,
	DOWNLOAD_TOKEN_EXPIRED
}
const map<TDownloadErrorCode, string> T_DOWNLOAD_ERROR_STR = {
	TDownloadErrorCode.DOWNLOAD_TOKEN_INVALID: "Download token invalid",
	TDownloadErrorCode.DOWNLOAD_TOKEN_EXPIRED: "Download token kadaluarsa"
}
exception TDownloadError{
	1: TDownloadErrorCode code;
}