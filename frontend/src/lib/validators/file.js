import { 
	TFileErrorCode, T_FILE_ERROR_STR,
} from '@/rpc/gen/file.file.errors_types';

export const FILE_NAME_REGEX = /^(?!\.)(?!com[0-9]$)(?!con$)(?!lpt[0-9]$)(?!nul$)(?!prn$)[^\|*\?\\:<>/$"]*[^\.\|*\?\\:<>/$"]+$/

export const FILE_NAME_RULES = [
	v => !!v || T_FILE_ERROR_STR[TFileErrorCode.FILE_NAME_EMPTY],
	v => FILE_NAME_REGEX.test(v) || T_FILE_ERROR_STR[TFileErrorCode.FILE_NAME_INVALID]
]