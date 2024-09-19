namespace py user.management.errors
namespace js user.management.errors

enum TUserManagementErrorCode{
    CANNOT_DELETE_VERIFIED,
    INSUFFICIENT_PERMISSION,
    INSUFFICIENT_PERMISSION_SET_ROLE,
    PASSWORD_EMPTY,
}
const map<TUserManagementErrorCode, string> T_AUTH_ERROR_STR = {
	TUserManagementErrorCode.CANNOT_DELETE_VERIFIED: "Tidak dapat menghapus akun yang telah terverifikasi",
	TUserManagementErrorCode.INSUFFICIENT_PERMISSION: "Anda tidak berhak melakukan ini pada user dengan peran lebih tinggi daripada Anda",
	TUserManagementErrorCode.INSUFFICIENT_PERMISSION_SET_ROLE: "Anda tidak berhak menentukan role yang lebih tinggi daripada Anda",
	TUserManagementErrorCode.PASSWORD_EMPTY: "Password kosong",
}
exception TUserManagementError{
	1: TUserManagementErrorCode code;
}
