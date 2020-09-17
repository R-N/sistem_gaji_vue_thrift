import TEmailService from '@/rpc/gen/TEmailService';
import { TBaseClient } from '@/rpc/client/base';


class TEmailServiceClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TEmailService, '/api/akun/email');
	}
	async has_password(token){
		//this.stores.helper.auth.requireLogout();
		return await this.client.has_password(token);
	}

	async verify_email(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.verify_email(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.user.get_user();
		}
	}

	async change_email(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.change_email(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.user.get_user();
		}
	}
	async set_password(token, password){
		//this.stores.helper.auth.requireLogout();
		await this.client.set_password(token, password);
		if (this.stores.auth.isLoggedIn){
			await this.stores.client.auth.login(
				this.stores.auth.user.username,
				password
			);
		}
	}
}

const emailClient = new TEmailServiceClient();

export { TEmailServiceClient, emailClient }
export default emailClient