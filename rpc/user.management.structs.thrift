include "user.user.types.thrift"

namespace py user.management.structs
namespace js user.management.structs

struct TUserRegistrationForm{
	1: string username;
	2: optional string password;
	3: string name;
	4: string email;
	5: user.user.types.TUserRole role;
}

struct TUserQuery{
	1: optional i32 limit;
	2: optional i32 offset;
	3: optional bool verified;
	4: optional bool enabled;
	5: optional user.user.types.TUserRole role;
}
