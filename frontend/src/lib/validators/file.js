import { 
	TFileErrorCode, T_FILE_ERROR_STR,
} from '@/rpc/gen/file.file.errors_types';
import errors from '@/rpc/gen/file.file.errors_types';
import { createRules, createRulesBase, createRulesFields } from "@/lib/validators/common";

export const FILE_NAME_REGEX_STR = /^(?!\.)(?!com[0-9]$)(?!con$)(?!lpt[0-9]$)(?!nul$)(?!prn$)[^\|*\?\\:<>/$"]*[^\.\|*\?\\:<>/$"]+$/

const RULES = createRulesFields(
	["FILE_NAME"],
	errors,
	{}, 
	TFileErrorCode, 
	T_FILE_ERROR_STR, 
	"FILE"
);
export default RULES;
