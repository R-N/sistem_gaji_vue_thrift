include "user.auth.errors.thrift"

namespace py hello.hello.services
namespace js hello.hello.services

service THelloService{
	string hello_admin_utama(
		1: string auth_token
	) throws (
		1: user.auth.errors.TAuthError auth_error
	);
}