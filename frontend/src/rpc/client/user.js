import TUserService from '@/rpc/gen/TUserService';
import { TBaseClient } from '@/rpc/client/base';


class TUserServiceClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserService, '/api/akun/user');
	}

	async get_user(){
		this.clientStore.auth.requireLogin();
		await this.authStore.setUser(
			await this.client.get_user(this.authStore.authToken)
		);
		return this.authStore.user;
	}
}

export { TUserServiceClient }
export default TUserServiceClient