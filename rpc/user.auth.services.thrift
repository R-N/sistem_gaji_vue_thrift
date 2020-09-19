include "user.auth.structs.thrift"
include "user.auth.errors.thrift"

namespace py user.auth.services
namespace js user.auth.services

service TUserAuthService{
	user.auth.structs.TLoginResult login(
		1: string username, 
		2: string password
	) throws (
		1: user.auth.errors.TLoginError login_error
	);

	string refresh_auth(
		1: string auth_token,
		2: string refresh_token
	) throws (
		1: user.auth.errors.TAuthError auth_error,
		2: user.auth.errors.TLoginError login_error
	);
}
