import { 
	TDepartemenErrorCode, T_DEPARTEMEN_ERROR_STR,
	NAME_MAX_LEN, 
	NAME_REGEX_STR
} from '@/rpc/gen/data.departemen.errors_types';
import { T_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'


export const NAME_REGEX = new RegExp(NAME_REGEX_STR);

export const NAME_RULES = [
	v => !!v || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAME_EMPTY],
	v => v.length <= NAME_MAX_LEN || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAME_TOO_LONG],
	v => NAME_REGEX.test(v) || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAME_INVALID]
]