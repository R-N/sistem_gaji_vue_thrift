include "data.departemen.errors.thrift"
include "data.departemen.structs.thrift"
include "user.auth.errors.thrift"

namespace py data.departemen.services
namespace js data.departemen.services

service TDataDepartemenService{
	list<data.departemen.structs.TDepartemen> fetch(
		1: string auth_token,
		2: data.departemen.structs.TDepartemenQuery query
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	data.departemen.structs.TDepartemen get(
		1: string auth_token,
		2: i32 departemen_id
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.departemen.errors.TDepartemenError departemen_error
	);

	data.departemen.structs.TDepartemen create(
		1: string auth_token,
		2: data.departemen.structs.TDepartemenForm form
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.departemen.errors.TDepartemenError departemen_error
	);

	void set_enabled(
		1: string auth_token,
		2: i32 departemen_id,
		3: bool enabled
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.departemen.errors.TDepartemenError departemen_error
	);

	void set_name(
		1: string auth_token,
		2: i32 departemen_id,
		3: string name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.departemen.errors.TDepartemenError departemen_error
	);

}