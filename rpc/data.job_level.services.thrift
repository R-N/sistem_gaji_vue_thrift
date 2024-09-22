include "data.job_level.errors.thrift"
include "data.job_level.structs.thrift"
include "user.auth.errors.thrift"

namespace py data.job_level.services
namespace js data.job_level.services

service TDataJobLevelService{
	list<data.job_level.structs.TJobLevel> fetch(
		1: string auth_token,
		2: data.job_level.structs.TJobLevelQuery query
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);

	data.job_level.structs.TJobLevel get(
		1: string auth_token,
		2: i32 job_level_id
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	data.job_level.structs.TJobLevel create(
		1: string auth_token,
		2: data.job_level.structs.TJobLevelForm form
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError jobLevel_error
	);

	void set_enabled(
		1: string auth_token,
		2: i32 job_level_id,
		3: bool enabled
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_name(
		1: string auth_token,
		2: i32 job_level_id,
		3: string name
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_gaji_pokok(
		1: string auth_token,
		2: i32 job_level_id,
		3: string gaji_pokok
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_tunjangan_jabatan(
		1: string auth_token,
		2: i32 job_level_id,
		3: string tunjangan_jabatan
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_upah_lembur_1(
		1: string auth_token,
		2: i32 job_level_id,
		3: string upah_lembur_1
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_upah_lembur_2(
		1: string auth_token,
		2: i32 job_level_id,
		3: string upah_lembur_2
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

	void set_upah_lembur_3(
		1: string auth_token,
		2: i32 job_level_id,
		3: string upah_lembur_3
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: data.job_level.errors.TJobLevelError job_level_error
	);

}