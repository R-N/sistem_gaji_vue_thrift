include "user.user.types.thrift"

namespace py user.user.structs
namespace js user.user.structs

struct TUser{
	1: i32 id;
	2: string username;
	3: user.user.types.TUserRole role;
	4: string name;
	5: string email;
	6: bool verified;
	7: bool enabled;
}
