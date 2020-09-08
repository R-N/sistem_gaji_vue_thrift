import AuthService from '@/rpc/gen/AuthService';
import { BaseClient } from '@/rpc/client/base';
import { UserRole, AuthError, AuthErrorCode, LoginError, LoginErrorCode } from '@/rpc/gen/auth_types';
import { authRouter } from '@/router/routers/auth';


const ERROR_NEED_REFRESH = [
	AuthErrorCode.AUTH_TOKEN_INVALID,
	AuthErrorCode.AUTH_TOKEN_EXPIRED
]
const ERROR_NEED_LOGIN = [
	LoginErrorCode.REFRESH_TOKEN_INVALID,
	LoginErrorCode.REFRESH_TOKEN_EXPIRED
]

class AuthServiceClient extends BaseClient{
	constructor(stores=null, authRefreshPeriod=9){
		super(stores, AuthService, '/api/akun/auth');
		this.authRefreshPeriod = authRefreshPeriod
	}

	requireLogin(){
		if (!this.authStore.authToken) throw new AuthError({ code: AuthErrorCode.NOT_LOGGED_IN });
	}
	requireLogout(){
		if (this.authStore.authToken) throw new LoginError({ code: LoginErrorCode.ALREADY_LOGGED_IN });
	}
	requireRole(role){
		if (!this.authStore.checkRole(role)) throw new AuthError({ code: AuthErrorCode.INVALID_ROLE });
	}

	async rehydrate(payload=null){
		if (!this.authStore.authToken) return true;
		if (this.authStore.dateChanged()){
			await this.logout();
			return false;
		}
		try{
			await this.refresh_auth();
			await this.get_user();
			await this.setAuthRefresher();
			return true;
		}catch(error){
			if ((error instanceof AuthError && ERROR_NEED_REFRESH.includes(error.code))
				|| (error instanceof LoginError && ERROR_NEED_LOGIN.includes(error.code))){
				await this.logout();
				throw new AuthError(AuthErrorCode.NOT_LOGGED_IN);
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
		return await this.get_user();
	}

	async setAuthRefresher(){
		if (!this.authStore.authRefresher){
			const cli = this;
			var authRefresher = window.setInterval(async function(){
				try{
					await cli.refresh_auth();
				}catch(error){
					cli.logout();
					if (error instanceof AuthError){
						if(error.code === AuthErrorCode.AUTH_TOKEN_EXPIRED){
							authRouter.dialogSessionExpired();
						}else{
							authRouter.dialogUnknownAuthError(error, error.code);
						}
					} else if (error instanceof LoginError){
						if(error.code === LoginErrorCode.REFRESH_TOKEN_EXPIRED){
							authRouter.dialogSessionExpired();
						}else{
							authRouter.dialogUnknownAuthError(error, error.code);
						}
					} else {
						authRouter.dialogUnknownError(error);
					}
				}
			}, this.authRefreshPeriod * 1000);
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

	async get_user(){
		this.requireLogin();
		await this.authStore.setUser(
			await this.client.get_user(this.authStore.authToken)
		);
		return this.authStore.user;
	}

	async hello_admin_utama(){
		this.requireRole(UserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(this.authStore.authToken);
	}

	authRefreshGuardAsync(target, name, descriptor) {
		const func = descriptor.value;
		const cli = this;
		descriptor.value = async function(...args) {
			cli.requireLogin();
			try{
				return await func.apply(this, args);
			}catch(error){
				if (error instanceof AuthError && error.code === AuthErrorCode.AUTH_TOKEN_EXPIRED){
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
				if (error instanceof AuthError && error.code === AuthErrorCode.AUTH_TOKEN_EXPIRED){
					await cli.refresh_auth();
					return func.apply(this, args);
				}
				throw error;
			}
		}
		return descriptor;
	}
}

export { AuthServiceClient }
export default AuthServiceClient