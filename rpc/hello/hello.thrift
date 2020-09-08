include "../akun/auth.thrift"

namespace py rpc.gen.hello
namespace js rpc.gen.hello

service THelloService{
	string hello_admin_utama(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);
}