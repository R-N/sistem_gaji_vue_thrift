import THelloService from '@/rpc/gen/THelloService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class THelloClient extends TBaseClient{
	constructor(stores=null){
		super(stores, THelloService, '/api/hello/hello');
		return this;
	}

	async hello_admin_utama(){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(this.authStore.authToken);
	}

}

const helloClient = new THelloClient();

export { THelloClient, helloClient }
export default helloClient