import { 
	TPerusahaanErrorCode, T_PERUSAHAAN_ERROR_STR,
} from '@/rpc/gen/data.perusahaan.errors_types';
import errors from '@/rpc/gen/data.perusahaan.errors_types';
import types from '@/rpc/gen/user.user.types_types';
import { createRules, createRulesBase } from "@/lib/validators/common";

// export const NAMA_RULES = [
// 	v => !!v || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_EMPTY],
// 	v => v.length <= NAMA_MAX_LEN || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_TOO_LONG],
// 	v => NAMA_REGEX.test(v) || T_PERUSAHAAN_ERROR_STR[TPerusahaanErrorCode.NAMA_INVALID]
// ]

export const createRulesField = (field) => createRules(
	field,
	createRulesBase(
		field,
		errors,
		types,
		TPerusahaanErrorCode,
		T_PERUSAHAAN_ERROR_STR,
		"PERUSAHAAN",
	),
	TPerusahaanErrorCode,
	T_PERUSAHAAN_ERROR_STR,
	"PERUSAHAAN",
);
export const NAMA_RULES = createRulesField("NAMA");
