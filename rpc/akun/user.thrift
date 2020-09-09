include "../akun/auth.thrift"

namespace py rpc.gen.akun.user
namespace js rpc.gen.akun.user

struct TUser{
	1: i32 id;
	2: string name;
	3: string email;
	4: auth.TUserRole role;
}
service TUserService{
	TUser get_user(
		1: string auth_token
	) throws (
		1: auth.TAuthError authError
	);
}