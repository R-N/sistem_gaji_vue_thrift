import { 
	TUserErrorCode, T_USER_ERROR_STR,
} from '@/rpc/gen/user.user.errors_types';
import errors from  '@/rpc/gen/user.user.errors_types';
import types from '@/rpc/gen/user.user.types_types';
import { createRules, createRulesBase, createRulesFields } from '@/lib/validators/common'

const RULES = createRulesFields(
	["USERNAME", "NAME", "PASSWORD", "EMAIL", "ROLE"],
	errors,
	types, 
	TUserErrorCode, 
	T_USER_ERROR_STR, 
	"USER"
);
export default RULES;
