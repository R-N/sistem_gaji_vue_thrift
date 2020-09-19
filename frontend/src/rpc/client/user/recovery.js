import TUserRecoveryService from '@/rpc/gen/TUserRecoveryService';
import { TBaseClient } from '@/rpc/client/base';


class TUserRecoveryClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserRecoveryService, '/api/user/recovery');
	}
	async reset_password(username){
		await this.client.reset_password(username);
	}
	async resend_verification(username){
		await this.client.resend_verification(username);
	}
}

const userRecoveryClient = new TUserRecoveryClient();

export { TUserRecoveryClient, userRecoveryClient }
export default userRecoveryClient