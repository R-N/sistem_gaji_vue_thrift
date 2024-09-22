include "data.perusahaan.errors.thrift"
include "data.perusahaan.structs.thrift"
include "user.auth.errors.thrift"

namespace py data.perusahaan.services
namespace js data.perusahaan.services

service TDataPerusahaanService{
	list<data.perusahaan.structs.TPerusahaan> fetch(
		1: string auth_token,
		2: data.perusahaan.structs.TPerusahaanQuery query
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	data.perusahaan.structs.TPerusahaan get(
		1: string auth_token,
		2: i32 perusahaan_id
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.perusahaan.errors.TPerusahaanError perusahaan_error
	);

	data.perusahaan.structs.TPerusahaan create(
		1: string auth_token,
		2: data.perusahaan.structs.TPerusahaanForm form
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.perusahaan.errors.TPerusahaanError perusahaan_error
	);

	void set_enabled(
		1: string auth_token,
		2: i32 perusahaan_id,
		3: bool enabled
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.perusahaan.errors.TPerusahaanError perusahaan_error
	);

	void set_name(
		1: string auth_token,
		2: i32 perusahaan_id,
		3: string name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.perusahaan.errors.TPerusahaanError perusahaan_error
	);

}