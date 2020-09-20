import TUserAuthService from '@/rpc/gen/TUserAuthService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';
import {  
	TAuthError, TAuthErrorCode, 
	TLoginError, TLoginErrorCode 
} from '@/rpc/gen/user.auth.errors_types';
import { authRouter } from '@/router/routers/auth';

class TUserAuthClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserAuthService, '/api/user/auth');
	}
	async login(username, password){
		await this.stores.app.setAuthBusy(true);
		try{
			let tokens = await this.client.login(username, password);
			await this.stores.auth.setTokens(tokens);
			await this.stores.helper.auth.setAuthRefresher();
			return await this.stores.client.user.profile.get_user();
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
			//await this.stores.app.setGlobalRefresh(true);
		}finally{
			await this.stores.app.setAuthBusy(false);
		}
	}
}

const userAuthClient = new TUserAuthClient();

export { TUserAuthClient, userAuthClient }
export default userAuthClient