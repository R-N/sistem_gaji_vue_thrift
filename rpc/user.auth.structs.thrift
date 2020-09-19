namespace py user.auth.structs
namespace js user.auth.structs

struct TLoginResult {
    1: string auth_token;
    2: optional string refresh_token;
}
