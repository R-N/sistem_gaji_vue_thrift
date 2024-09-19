import { 
	TJobLevelErrorCode, T_JOB_LEVEL_ERROR_STR,
	NAMA_LEN_MAX, 
	NAMA_REGEX_STR,
	MONEY_LEN_MAX,
} from '@/rpc/gen/data.job_level.errors_types';
import { T_USER_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'


export const NAMA_REGEX = new RegExp(NAMA_REGEX_STR);

export const NAMA_RULES = [
	v => !!v || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAMA_EMPTY],
	v => v.length <= NAMA_LEN_MAX || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAMA_TOO_LONG],
	v => NAMA_REGEX.test(v) || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAMA_INVALID]
]
export const GAJI_POKOK_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.GAJI_POKOK_INVALID],
]
export const TUNJANGAN_JABATAN_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.TUNJANGAN_JABATAN_INVALID],
]
export const UPAH_LEMBUR_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.UPAH_LEMBUR_INVALID],
]
export const UPAH_LEMBUR_RULES_2 = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.UPAH_LEMBUR_INVALID_2],
]
export const UPAH_LEMBUR_1_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.UPAH_LEMBUR_1_INVALID],
]
export const UPAH_LEMBUR_2_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.UPAH_LEMBUR_2_INVALID],
]
export const UPAH_LEMBUR_3_RULES = [
	v => parseInt(v) >= 0 || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.UPAH_LEMBUR_3_INVALID],
]
