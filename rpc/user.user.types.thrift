namespace py user.user.types
namespace js user.user.types

enum TUserRole{
	ZERO,
	KARYAWAN,
	ADMIN_BIASA,
	ADMIN_UTAMA,
	ADMIN_AKUN,
	PENGAWAS,
	SUPER_ADMIN
}
const map<TUserRole, string> T_USER_ROLE_STR = {
	TUserRole.KARYAWAN: "Karyawan",
	TUserRole.ADMIN_BIASA: "Admin Biasa",
	TUserRole.ADMIN_UTAMA: "Admin Utama",
	TUserRole.ADMIN_AKUN: "Admin Akun",
	TUserRole.PENGAWAS: "Pengawas",
	TUserRole.SUPER_ADMIN: "Super Admin"
}
const map<TUserRole, list<TUserRole>> T_USER_ROLE_DOUBLES = {
	TUserRole.KARYAWAN: [TUserRole.KARYAWAN, TUserRole.ADMIN_BIASA, TUserRole.ADMIN_UTAMA, TUserRole.ADMIN_AKUN, TUserRole.PENGAWAS, TUserRole.SUPER_ADMIN],
	TUserRole.ADMIN_BIASA: [TUserRole.ADMIN_BIASA, TUserRole.ADMIN_UTAMA, TUserRole.SUPER_ADMIN],
	TUserRole.ADMIN_UTAMA: [TUserRole.ADMIN_UTAMA, TUserRole.SUPER_ADMIN],
	TUserRole.ADMIN_AKUN: [TUserRole.ADMIN_AKUN, TUserRole.ADMIN_UTAMA, TUserRole.SUPER_ADMIN],
	TUserRole.PENGAWAS: [TUserRole.ADMIN_UTAMA, TUserRole.PENGAWAS, TUserRole.SUPER_ADMIN],
	TUserRole.SUPER_ADMIN: [TUserRole.SUPER_ADMIN]
}
