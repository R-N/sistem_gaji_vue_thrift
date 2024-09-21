import { 
	TPerusahaanErrorCode, T_PERUSAHAAN_ERROR_STR,
} from '@/rpc/gen/data.perusahaan.errors_types';
import errors from '@/rpc/gen/data.perusahaan.errors_types';
import types from '@/rpc/gen/user.user.types_types';
import { createRulesField as _createRulesField, createRulesFields } from "@/lib/validators/common";

export const createRulesField = (field) => _createRulesField(
	field,
	errors,
	types, 
	TPerusahaanErrorCode, 
	T_PERUSAHAAN_ERROR_STR, 
	"PERUSAHAAN"
);
export const NAMA_RULES = createRulesField("NAMA");

const RULES = createRulesFields(
	["NAMA"],
	errors,
	types, 
	TPerusahaanErrorCode, 
	T_PERUSAHAAN_ERROR_STR, 
	"PERUSAHAAN"
);
export default RULES;
