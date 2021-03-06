import { 
	TPerusahaanErrorCode, T_PERUSAHAAN_ERROR_STR,
	NAMA_LEN_MAX, 
	NAMA_REGEX_STR
} from '@/rpc/gen/data.perusahaan.errors_types';
import { T_USER_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'


export const NAMA_REGEX = new RegExp(NAMA_REGEX_STR);

export const NAMA_RULES = [
	v => !!v || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_EMPTY],
	v => v.length <= NAMA_LEN_MAX || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_TOO_LONG],
	v => NAMA_REGEX.test(v) || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_INVALID]
]