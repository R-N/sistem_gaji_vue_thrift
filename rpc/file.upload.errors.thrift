namespace py file.upload.errors
namespace js file.upload.errors

enum TUploadErrorCode{
	UPLOAD_TOKEN_INVALID,
	UPLOAD_TOKEN_EXPIRED,
	FILE_NOT_PROVIDED,
	FILE_INVALID
}
const map<TUploadErrorCode, string> T_UPLOAD_ERROR_STR = {
	TUploadErrorCode.UPLOAD_TOKEN_INVALID: "Upload token invalid",
	TUploadErrorCode.UPLOAD_TOKEN_EXPIRED: "Upload token kadaluarsa",
	TUploadErrorCode.FILE_NOT_PROVIDED: "Anda belum memilih file",
	TUploadErrorCode.FILE_INVALID: "File tidak valid"
}
exception TUploadError{
	1: TUploadErrorCode code;
}