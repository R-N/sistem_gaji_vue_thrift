import { 
	TUserErrorCode, T_USER_ERROR_STR,
} from '@/rpc/gen/user.user.errors_types';
import errors from  '@/rpc/gen/user.user.errors_types';
import types from '@/rpc/gen/user.user.types_types';
import { createRules, createRulesBase } from '@/lib/validators/common'

export const createRulesField = (field) => createRules(
	field,
	createRulesBase(
		field,
		errors,
		types,
		TUserErrorCode,
		T_USER_ERROR_STR,
		"USER",
	),
	TUserErrorCode,
	T_USER_ERROR_STR,
	"USER",
);

export const USERNAME_RULES = createRulesField("USERNAME");
export const NAME_RULES = createRulesField("NAME");
export const PASSWORD_RULES = createRulesField("PASSWORD");
export const EMAIL_RULES = createRulesField("EMAIL");
export const ROLE_RULES = createRulesField("ROLE");

