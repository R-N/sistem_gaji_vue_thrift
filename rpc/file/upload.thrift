namespace py rpc.gen.file.upload
namespace js rpc.gen.file.upload

enum TUploadErrorCode{
	UPLOAD_TOKEN_INVALID,
	UPLOAD_TOKEN_EXPIRED
}
const map<TUploadErrorCode, string> T_UPLOAD_ERROR_STR = {
	TUploadErrorCode.UPLOAD_TOKEN_INVALID: "Upload token invalid",
	TUploadErrorCode.UPLOAD_TOKEN_EXPIRED: "Upload token kadaluarsa"
}
exception TUploadError{
	1: TUploadErrorCode code;
}