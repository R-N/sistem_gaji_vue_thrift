import { 
	TUserErrorCode, T_USER_ERROR_STR,
	USERNAME_LEN_MAX,
	PASSWORD_LEN_MIN,
	PASSWORD_LEN_MAX,
	NAME_LEN_MAX,
	EMAIL_LEN_MAX,
	EMAIL_REGEX_STR,
	PASSWORD_REGEX_STR,
	USERNAME_REGEX_STR,
	NAME_REGEX_STR
} from '@/rpc/gen/user.user.errors_types';
import { T_USER_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'

export const EMAIL_REGEX = new RegExp(EMAIL_REGEX_STR);
export const PASSWORD_REGEX = new RegExp(PASSWORD_REGEX_STR);
export const USERNAME_REGEX = new RegExp(USERNAME_REGEX_STR);
export const NAME_REGEX = new RegExp(NAME_REGEX_STR);

export const USERNAME_RULES = [
	v => !!v || T_USER_ERROR_STR[TUserErrorCode.USERNAME_EMPTY],
	v => v.length <= USERNAME_LEN_MAX || T_USER_ERROR_STR[TUserErrorCode.USERNAME_TOO_LONG],
	v => USERNAME_REGEX.test(v) || T_USER_ERROR_STR[TUserErrorCode.USERNAME_INVALID]
]
export const NAME_RULES = [
	v => !!v || T_USER_ERROR_STR[TUserErrorCode.NAME_EMPTY],
	v => v.length <= NAME_LEN_MAX || T_USER_ERROR_STR[TUserErrorCode.NAME_TOO_LONG],
	v => NAME_REGEX.test(v) || T_USER_ERROR_STR[TUserErrorCode.NAME_INVALID]
]
export const PASSWORD_RULES = [
	v => !!v || T_USER_ERROR_STR[TUserErrorCode.PASSWORD_EMPTY],
	v => v.length <= PASSWORD_LEN_MAX || T_USER_ERROR_STR[TUserErrorCode.PASSWORD_TOO_LONG],
	v => v.length >= PASSWORD_LEN_MIN || T_USER_ERROR_STR[TUserErrorCode.PASSWORD_TOO_SHORT],
	v => PASSWORD_REGEX.test(v) || T_USER_ERROR_STR[TUserErrorCode.PASSWORD_INVALID]
]
export const EMAIL_RULES = [
	v => !!v || T_USER_ERROR_STR[TUserErrorCode.EMAIL_EMPTY],
	v => v.length <= EMAIL_LEN_MAX || T_USER_ERROR_STR[TUserErrorCode.EMAIL_TOO_LONG],
	v => EMAIL_REGEX.test(v) || T_USER_ERROR_STR[TUserErrorCode.EMAIL_INVALID]
]
export const ROLE_RULES = [
	v => (v !== undefined && v !== null) || T_USER_ERROR_STR[TUserErrorCode.ROLE_EMPTY],
	v => (isInt(v) && (v in T_USER_ROLE_STR)) || T_USER_ERROR_STR[TUserErrorCode.ROLE_INVALID]
]