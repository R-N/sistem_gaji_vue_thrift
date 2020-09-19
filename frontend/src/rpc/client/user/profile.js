import TUserProfileService from '@/rpc/gen/TUserProfileService';
import { TBaseClient } from '@/rpc/client/base';


class TUserProfileClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserProfileService, '/api/user/profile');
	}

	async get_user(){
		this.stores.helper.auth.requireLogin();
		let user = await this.client.get_user(this.stores.auth.authToken)
		await this.stores.auth.setUser(user);
		return this.stores.auth.user;
	}

	async change_email(email){
		this.stores.helper.auth.requireLogin();
		await this.client.change_email(this.stores.auth.authToken, email)
		//await this.stores.auth.setUserEmail(email);
	}
	async set_password(old_password, new_password){
		this.stores.helper.auth.requireLogin();
		let tokens = await this.client.set_password(
			this.stores.auth.authToken, 
			old_password,
			new_password
		);
		await this.stores.auth.setTokens(tokens);
	}
	async set_name(name){
		this.stores.helper.auth.requireLogin();
		await this.client.set_name(this.stores.auth.authToken, name)
		await this.stores.auth.setUserName(name);
	}

}

const userProfileClient = new TUserProfileClient();

export { TUserProfileClient, userProfileClient }
export default userProfileClient