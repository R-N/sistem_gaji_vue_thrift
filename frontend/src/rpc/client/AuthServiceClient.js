import AuthService from '@/rpc/gen/AuthService';
import { BaseClient } from '@/rpc/client/BaseClient';
import { authStore } from "@/store/modules/auth";
import { UserRole, AuthError, AuthErrorCode, LoginError, LoginErrorCode } from '@/rpc/gen/auth_types';


const ERROR_NEED_REFRESH = [
	AuthErrorCode.AUTH_TOKEN_INVALID,
	AuthErrorCode.AUTH_TOKEN_EXPIRED
]
const ERROR_NEED_LOGIN = [
	LoginErrorCode.REFRESH_TOKEN_INVALID,
	LoginErrorCode.REFRESH_TOKEN_EXPIRED
]

class AuthServiceClient extends BaseClient{
	constructor(){
		super(AuthService, '/api/akun/auth');
		this.authStore = authStore;
	}

	requireLogin(){
		if (!authStore.authToken) throw new AuthError({ code: AuthErrorCode.NOT_LOGGED_IN });
	}
	requireLogout(){
		if (authStore.authToken) throw new LoginError({ code: LoginErrorCode.ALREADY_LOGGED_IN });
	}
	requireRole(){
		if (!authStore.checkRole(role)) throw new AuthError({ code: AuthErrorCode.INVALID_ROLE });
	}

	async rehydrate(payload=null){
		if (!authStore.authToken) return;
		try{
			await this.refresh_auth();
			await this.get_user();
			await this.setAuthRefresher();
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
		console.log("Pre login");
		await authStore.setTokens(
			await this.client.login(username, password)
		);
		console.log("Pre setAuthRefresher");
		await this.setAuthRefresher();
		console.log("Pre get_user");
		return await this.get_user();
	}

	async setAuthRefresher(){
		if (!authStore.authRefresher){
			const cli = this;
			var authRefresher = window.setInterval(async function(){
				await cli.refresh_auth();
			}, 1000);
			await authStore.setAuthRefresher(authRefresher);
		}
	}

	async logout(){
		await authStore.logout();
	}

	async refresh_auth(){
		this.requireLogin();
		await authStore.setAuthToken(
			await this.client.refresh_auth(authStore.authToken, authStore.refreshToken)
		);
		await this.setAuthRefresher();
	}

	async get_user(){
		this.requireLogin();
		await authStore.setUser(
			await this.client.get_user(authStore.authToken)
		);
		return authStore.user;
	}

	async hello_admin_utama(){
		this.requireRole(UserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(authStore.authToken);
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