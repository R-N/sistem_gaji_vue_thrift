import { 
	TDepartemenErrorCode, T_DEPARTEMEN_ERROR_STR,
} from '@/rpc/gen/data.departemen.errors_types';
import errors from '@/rpc/gen/data.departemen.errors_types';
import types from '@/rpc/gen/user.user.types_types';
import { createRulesField as _createRulesField, createRulesFields } from "@/lib/validators/common";

export const createRulesField = (field) => _createRulesField(
	field,
	errors,
	types, 
	TDepartemenErrorCode, 
	T_DEPARTEMEN_ERROR_STR, 
	"DEPARTEMEN"
);
export const NAME_RULES = createRulesField("NAME");

const RULES = createRulesFields(
	["NAME"],
	errors,
	types, 
	TDepartemenErrorCode, 
	T_DEPARTEMEN_ERROR_STR, 
	"DEPARTEMEN"
);
export default RULES;
