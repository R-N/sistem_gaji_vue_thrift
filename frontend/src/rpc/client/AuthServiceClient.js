import AuthService from '@/rpc/gen/AuthService';
import { BaseClient } from '@/rpc/client/BaseClient';
import { authStore, requireLogin, requireRole, requireLogout } from "@/store/modules/auth";
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
		super(AuthService, '/api/auth');
		this.authStore = authStore;
	}

	async rehydrate(payload=null){
		if (!authStore.authToken) return;
		try{
			await this.refresh_auth();
			await this.get_user();
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
		await authStore.setTokens(
			await this.client.login(username, password)
		);
		await this.setAuthRefresher();
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

	@requireLogin()
	async refresh_auth(){
		await authStore.setAuthToken(
			await this.client.refresh_auth(authStore.authToken, authStore.refreshToken)
		);
		await this.setAuthRefresher();
	}

	@requireLogin()
	async get_user(){
		await authStore.setUser(
			await this.client.get_user(authStore.authToken)
		);
		return authStore.user;
	}

	@requireRole(UserRole.ADMIN_UTAMA)
	async hello_admin_utama(){
		return await this.client.hello_admin_utama(authStore.authToken);
	}
}

export { AuthServiceClient, requireLogin, requireRole, requireLogout }
export default AuthServiceClient