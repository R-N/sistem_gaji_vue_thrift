import THelloService from '@/rpc/gen/THelloService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/auth_types';


class THelloServiceClient extends TBaseClient{
	constructor(stores=null){
		super(stores, THelloService, '/api/hello/hello');
		return this;
	}

	async rehydrate(payload=null){
	}
	async hello_admin_utama(){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(this.authStore.authToken);
	}

}

export { THelloServiceClient }
export default THelloServiceClient