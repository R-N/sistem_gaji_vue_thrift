import TAuthService from '@/rpc/gen/TAuthService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole, TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from '@/rpc/gen/auth_types';
import { authRouter } from '@/router/routers/auth';

const ERROR_NEED_REFRESH = [
	TAuthErrorCode.AUTH_TOKEN_INVALID,
	TAuthErrorCode.AUTH_TOKEN_EXPIRED
]
const ERROR_NEED_LOGIN = [
	TLoginErrorCode.REFRESH_TOKEN_INVALID,
	TLoginErrorCode.REFRESH_TOKEN_EXPIRED
]

class TAuthServiceClient extends TBaseClient{
	constructor(stores=null, authRefreshPeriod=9){
		super(stores, TAuthService, '/api/akun/auth');
		this.authRefreshPeriod = authRefreshPeriod
	}

	requireLogin(){
		if (!this.authStore.authToken) throw new TAuthError({ code: TAuthErrorCode.NOT_LOGGED_IN });
	}
	requireLogout(){
		if (this.authStore.authToken) throw new TLoginError({ code: TLoginErrorCode.ALREADY_LOGGED_IN });
	}
	requireRole(role){
		this.requireLogin();
		if (!this.authStore.checkRole(role)) throw new TAuthError({ code: TAuthErrorCode.INVALID_ROLE });
	}

	async rehydrate(payload=null){
		if (!this.authStore.authToken) return true;
		if (this.authStore.dateChanged()){
			await this.logout();
			return false;
		}
		try{
			await this.refresh_auth();
			await this.clientStore.user.get_user();
			await this.setAuthRefresher();
			return true;
		}catch(error){
			if ((error instanceof TAuthError && ERROR_NEED_REFRESH.includes(error.code))
				|| (error instanceof TLoginError && ERROR_NEED_LOGIN.includes(error.code))){
				await this.logout();
				throw new TAuthError(TAuthErrorCode.NOT_LOGGED_IN);
			}else{
				throw error;
			}
		}
	}
	async login(username, password){
		await this.authStore.setTokens(
			await this.client.login(username, password)
		);
		await this.setAuthRefresher();
		return await this.clientStore.user.get_user();
	}

	async setAuthRefresher(){
		if (!this.authStore.authRefresher){
			const cli = this;
			var authRefresher = window.setInterval(async function(){
				try{
					await cli.refresh_auth();
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
			await this.authStore.setAuthRefresher(authRefresher);
		}
	}

	async logout(){
		await this.authStore.logout();
		await this.appStore.setGlobalLogout(true);
	}

	async refresh_auth(){
		this.requireLogin();
		const newToken = await this.client.refresh_auth(this.authStore.authToken, this.authStore.refreshToken);
		await this.authStore.setAuthToken(newToken);
		await this.setAuthRefresher();
	}

	authRefreshGuardAsync(target, name, descriptor) {
		const func = descriptor.value;
		const cli = this;
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

	//Everything that access API should be async
	authRefreshGuard(target, name, descriptor) {
		const func = descriptor.value;
		const cli = this;
		descriptor.value = async function(...args) {
			cli.requireLogin();
			try{
				return func.apply(this, args);
			}catch(error){
				if (error instanceof TAuthError && error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
					await cli.refresh_auth();
					return func.apply(this, args);
				}
				throw error;
			}
		}
		return descriptor;
	}
}

export { TAuthServiceClient }
export default TAuthServiceClient