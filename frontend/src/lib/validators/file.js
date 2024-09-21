import { 
	TFileErrorCode, T_FILE_ERROR_STR,
} from '@/rpc/gen/file.file.errors_types';
import errors from '@/rpc/gen/file.file.errors_types';
import { createRules, createRulesBase } from "@/lib/validators/common";

export const FILE_NAME_REGEX_STR = /^(?!\.)(?!com[0-9]$)(?!con$)(?!lpt[0-9]$)(?!nul$)(?!prn$)[^\|*\?\\:<>/$"]*[^\.\|*\?\\:<>/$"]+$/

export const createRulesField = (field) => createRules(
	field,
	createRulesBase(
		field,
		errors,
		{},
		TFileErrorCode,
		T_FILE_ERROR_STR,
		"FILE",
	),
	TFileErrorCode,
	T_FILE_ERROR_STR,
	"FILE",
);
export const FILE_NAME_RULES = createRulesField("FILE_NAME");
