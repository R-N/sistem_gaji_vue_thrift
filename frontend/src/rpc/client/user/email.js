import TUserEmailService from '@/rpc/gen/TUserEmailService';
import { TBaseClient } from '@/rpc/client/base';


class TUserEmailClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserEmailService, '/api/user/email');
	}
	async has_password(token){
		//this.stores.helper.auth.requireLogout();
		return await this.client.has_password(token);
	}

	async verify_email(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.verify_email(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.user.profile.get_user();
		}
	}

	async change_email(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.change_email(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.user.profile.get_user();
		}
	}
	async set_password(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.set_password(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.user.auth.login(
				this.stores.auth.user.username,
				password
			);
		}
	}
}

const userEmailClient = new TUserEmailClient();

export { TUserEmailClient, userEmailClient }
export default userEmailClient