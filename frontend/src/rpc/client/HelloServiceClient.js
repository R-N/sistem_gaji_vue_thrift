import HelloService from '@/rpc/gen/HelloService';
import { BaseClient } from '@/rpc/client/BaseClient';
import { authStore, clientStore } from "@/store/stores";
import { UserRole } from '@/rpc/gen/auth_types';


class HelloServiceClient extends BaseClient{
	constructor(){
		super(HelloService, '/api/hello/hello');
		this.authStore = authStore;
		this.clientStore = clientStore;
	}

	async rehydrate(payload=null){
	}
	async hello_admin_utama(){
		clientStore.auth.requireRole(UserRole.ADMIN_UTAMA);
		return await this.client.hello_admin_utama(authStore.authToken);
	}

}

export { HelloServiceClient }
export default HelloServiceClient