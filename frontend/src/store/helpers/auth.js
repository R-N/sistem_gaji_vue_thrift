import { 
	TAuthError, TAuthErrorCode, 
	TLoginError, TLoginErrorCode 
} from '@/rpc/gen/user.auth.errors_types';
import { TUserRole } from '@/rpc/gen/user.user.types_types';

import { authRouter } from '@/router/routers/auth';
import { StoreUser } from '@/store/user';

const ERROR_NEED_REFRESH = [
	TAuthErrorCode.AUTH_TOKEN_INVALID,
	TAuthErrorCode.AUTH_TOKEN_EXPIRED
]
const ERROR_NEED_LOGIN = [
	TLoginErrorCode.REFRESH_TOKEN_INVALID,
	TLoginErrorCode.REFRESH_TOKEN_EXPIRED
]

class AuthHelper extends StoreUser{
	constructor(stores=null, authRefreshPeriod=4){
		super(stores);
		this.authRefreshPeriod = authRefreshPeriod
	}
	requireLogin(){
		if (!this.stores.auth.authToken) throw new TAuthError({ code: TAuthErrorCode.NOT_LOGGED_IN });
	}
	requireLogout(){
		if (this.stores.auth.authToken) throw new TLoginError({ code: TLoginErrorCode.ALREADY_LOGGED_IN });
	}
	requireRole(role){
		this.requireLogin();
		if (!this.stores.auth.checkRole(role)) throw new TAuthError({ code: TAuthErrorCode.ROLE_INVALID });
	}

	async rehydrate(payload=null){
		if (!this.stores.auth.authToken) return true;
		if (this.stores.auth.dateChanged()){
			await this.stores.client.user.auth.logout();
			return false;
		}
		try{
			await this.stores.client.user.auth.refresh_auth();
			await this.stores.client.user.profile.get_user();
			await this.stores.helper.settings.getSettings();
			await this.setAuthRefresher();
			return true;
		}catch(error){
			if ((error instanceof TAuthError && ERROR_NEED_REFRESH.includes(error.code))
				|| (error instanceof TLoginError && ERROR_NEED_LOGIN.includes(error.code))){
				await this.stores.client.user.auth.logout();
				throw new TLoginError({ code: TLoginErrorCode.REFRESH_TOKEN_EXPIRED });
			}else{
				throw error;
			}
		}
	}

	async setAuthRefresher(){
		if (!this.stores.auth.authRefresher){
			const cli = this.stores.client.user.auth;
			const cli2 = this.stores.helper.settings;
			var authRefresher = window.setInterval(async function(){
				try{
					await cli.refresh_auth();
					await cli2.getSettings();
				}catch(error){
					cli.logout();
					if (error instanceof TAuthError){
						if(error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
							authRouter.dialogSessionExpired();
						}else{
							authRouter.dialogUnknownTAuthError(error, error.code);
						}
					} else if (error instanceof TLoginError){
						if(error.code === TLoginErrorCode.REFRESH_TOKEN_EXPIRED){
							authRouter.dialogSessionExpired();
						}else{
							authRouter.dialogUnknownTAuthError(error, error.code);
						}
					} else {
						authRouter.dialogUnknownError(error);
					}
				}
			}, this.authRefreshPeriod * 60 * 1000);
			await this.stores.auth.setAuthRefresher(authRefresher);
		}
	}
	authRefreshGuard(target, name, descriptor) {
		const func = descriptor.value;
		const cli = this.stores.client.user.auth;
		descriptor.value = async function(...args) {
			cli.requireLogin();
			try{
				return await func.apply(this, args);
			}catch(error){
				if (error instanceof TAuthError && error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
					await cli.refresh_auth();
					return await func.apply(this, args);
				}
				throw error;
			}
		}
		return descriptor;
	}
}

const authHelper = new AuthHelper();

export { AuthHelper, authHelper }
export default authHelper