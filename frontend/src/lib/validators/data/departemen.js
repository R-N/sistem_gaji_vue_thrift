import { 
	TDepartemenErrorCode, T_DEPARTEMEN_ERROR_STR,
	NAMA_MAX_LEN, 
	NAMA_REGEX_STR
} from '@/rpc/gen/data.departemen.errors_types';
import { T_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'


export const NAMA_REGEX = new RegExp(NAMA_REGEX_STR);

export const NAMA_RULES = [
	v => !!v || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAMA_EMPTY],
	v => v.length <= NAMA_MAX_LEN || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAMA_TOO_LONG],
	v => NAMA_REGEX.test(v) || T_DEPARTEMEN_ERROR_STR[TDepartemenErrorCode.NAMA_INVALID]
]