import { 
	TJobLevelErrorCode, T_JOB_LEVEL_ERROR_STR,
	NAME_MAX_LEN, 
	NAME_REGEX_STR,
	MONEY_MAX_LEN,
} from '@/rpc/gen/data.job_level.errors_types';
import { T_ROLE_STR } from '@/rpc/gen/user.user.types_types';
import { isInt } from '@/lib/util'


export const NAME_REGEX = new RegExp(NAME_REGEX_STR);

export const NAME_RULES = [
	v => !!v || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAME_EMPTY],
	v => v.length <= NAME_MAX_LEN || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAME_TOO_LONG],
	v => NAME_REGEX.test(v) || T_JOB_LEVEL_ERROR_STR[TJobLevelErrorCode.NAME_INVALID]
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
