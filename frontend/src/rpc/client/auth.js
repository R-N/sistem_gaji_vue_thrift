import TAuthService from '@/rpc/gen/TAuthService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole, TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from '@/rpc/gen/auth_types';
import { authRouter } from '@/router/routers/auth';

class TAuthServiceClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TAuthService, '/api/akun/auth');
	}
	async login(username, password){
		await this.stores.app.setAuthBusy(true);
		try{
			let tokens = await this.client.login(username, password);
			await this.stores.auth.setTokens(tokens);
			await this.stores.helper.auth.setAuthRefresher();
			return await this.stores.client.user.get_user();
		}finally{
			await this.stores.app.setAuthBusy(false);
		}
	}
	async refresh_auth(){
		this.stores.helper.auth.requireLogin();
		const newAuth = await this.client.refresh_auth(this.stores.auth.authToken, this.stores.auth.refreshToken);
		await this.stores.auth.setAuthToken(newAuth);
		await this.stores.helper.auth.setAuthRefresher();
	}
	async logout(){
		await this.stores.app.setAuthBusy(true);
		try{
			await this.stores.auth.logout();
			await this.stores.app.setGlobalLogout(true);
		}finally{
			await this.stores.app.setAuthBusy(false);
		}
	}
	async reset_password(username){
		await this.client.reset_password(username);
	}
	async resend_verification(username){
		await this.client.resend_verification(username);
	}
}

const authClient = new TAuthServiceClient();

export { TAuthServiceClient, authClient }
export default authClient