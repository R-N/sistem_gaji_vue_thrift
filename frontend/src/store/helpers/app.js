import { TUserRole, TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from '@/rpc/gen/auth_types';
import { authRouter } from '@/router/routers/auth';
import { StoreUser } from '@/store/user';

class AppHelper extends StoreUser{
	constructor(stores=null){
		super(stores);
	}
	handleError(error){
		if (error instanceof TLoginError){
			if (error.code === TLoginErrorCode.ALREADY_LOGGED_IN){
				return authRouter.dialogRequireLogout();
			} else if (error.code === TLoginErrorCode.REFRESH_TOKEN_EXPIRED){
				this.stores.client.auth.logout();
				return authRouter.dialogSessionExpired();
			} else {
				console.log(error);
				this.stores.client.auth.logout();
				return authRouter.dialogUnknownTAuthError("TLoginError", error.code);
			}
		} else if (error instanceof TAuthError){
			if (error.code === TAuthErrorCode.ROLE_INVALID){
				return authRouter.dialogRequireRole();
			} else if (error.code === TAuthErrorCode.NOT_LOGGED_IN){
				this.stores.client.auth.logout();
				return authRouter.dialogRequireLogin();
			} else if (error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
				this.stores.client.auth.logout();
				return authRouter.dialogAuthExpired();
			} else {
				console.log(error);
				this.stores.client.auth.logout();
				return authRouter.dialogUnknownTAuthError("TAuthError", error.code);
			}
		} else {
			console.log(error);
			return authRouter.dialogUnknownError(error);
		}
	}
}

const appHelper = new AppHelper();

export { AppHelper, appHelper }
export default appHelper