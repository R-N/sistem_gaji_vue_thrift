import HelloService from '@/rpc/gen/HelloService';
import { BaseClient } from '@/rpc/client/base';
import { UserRole } from '@/rpc/gen/auth_types';


class HelloServiceClient extends BaseClient{
	constructor(stores=null){
		super(stores, HelloService, '/api/hello/hello');
		return this;
	}

	async rehydrate(payload=null){
	}
	async hello_admin_utama(){
		this.clientStore.auth.requireRole(UserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(this.authStore.authToken);
	}

}

export { HelloServiceClient }
export default HelloServiceClient