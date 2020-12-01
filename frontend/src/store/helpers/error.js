import { 
	TAuthError, TAuthErrorCode, T_AUTH_ERROR_STR,
	TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR
} from '@/rpc/gen/user.auth.errors_types';
import { 
	TUserError, T_USER_ERROR_STR
} from '@/rpc/gen/user.user.errors_types';
import { 
	TUserEmailError, T_USER_EMAIL_ERROR_STR
} from '@/rpc/gen/user.email.errors_types';
import { 
	TEmailError, T_EMAIL_ERROR_STR
} from '@/rpc/gen/email.errors_types';
import { 
	TDownloadError, T_DOWNLOAD_ERROR_STR
} from '@/rpc/gen/file.download.errors_types';
import { 
	TUploadError, T_UPLOAD_ERROR_STR
} from '@/rpc/gen/file.upload.errors_types';
import { 
	TFileError, T_FILE_ERROR_STR
} from '@/rpc/gen/file.file.errors_types';
import { 
	TPerusahaanError, T_PERUSAHAAN_ERROR_STR
} from '@/rpc/gen/data.perusahaan.errors_types';

import { TUserRole } from '@/rpc/gen/user.user.types_types';

import { authRouter } from '@/router/routers/auth';
import { router } from '@/router/index';
import { StoreUser } from '@/store/user';

const T_ERROR_STR = {
	TAuthError: T_AUTH_ERROR_STR,
	TLoginError: T_LOGIN_ERROR_STR,
	TUserError: T_USER_ERROR_STR,
	TUserEmailError: T_USER_EMAIL_ERROR_STR,
	TEmailError: T_EMAIL_ERROR_STR,
	TDownloadError: T_DOWNLOAD_ERROR_STR,
	TUploadError: T_UPLOAD_ERROR_STR,
	TFileError: T_FILE_ERROR_STR,
	TPerusahaanError: T_PERUSAHAAN_ERROR_STR
}

class ErrorHelper extends StoreUser{
	constructor(stores=null){
		super(stores);
	}
	showError(message, route=null){
		let msg = {
			title: "Error",
			text: message
		}
		if (route){
			msg.onDismiss = function(){
				router.safePush({
					name: route
				});
			}
		}
		this.stores.app.pushTabDialog(msg);
	}
	getErrorName(error){
		return error.name.substring(error.name.lastIndexOf('.') + 1);
	}
	showErrorReturn(message){
		return this.showError(message, "beranda");
	}
	showFilteredError(error, classes=null, route=null){
		if (!classes || classes.includes(error.constructor)){
			let errorName = this.getErrorName(error);
			this.showError(T_ERROR_STR[errorName][error.code], route);
			return true;
		}
		return false;
	}
	handleUncaughtError(error){
		if (error instanceof TLoginError){
			if (error.code === TLoginErrorCode.ALREADY_LOGGED_IN){
				return authRouter.dialogRequireLogout();
			} else if (error.code === TLoginErrorCode.REFRESH_TOKEN_EXPIRED){
				this.stores.client.user.auth.logout();
				return authRouter.dialogSessionExpired();
			} else {
				console.log(error);
				this.stores.client.user.auth.logout();
				return authRouter.dialogUnknownTAuthError("TLoginError", error.code);
			}
		} else if (error instanceof TAuthError){
			if (error.code === TAuthErrorCode.ROLE_INVALID){
				return authRouter.dialogRequireRole();
			} else if (error.code === TAuthErrorCode.NOT_LOGGED_IN){
				this.stores.client.user.auth.logout();
				return authRouter.dialogRequireLogin();
			} else if (error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
				this.stores.client.user.auth.logout();
				return authRouter.dialogAuthExpired();
			} else {
				console.log(error);
				this.stores.client.user.auth.logout();
				return authRouter.dialogUnknownTAuthError("TAuthError", error.code);
			}
		} else {
			console.log(error);
			return authRouter.dialogUnknownError(error);
		}
	}
}

const errorHelper = new ErrorHelper();

export { ErrorHelper, errorHelper, T_ERROR_STR }
export default errorHelper