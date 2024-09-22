import TDataDepartemenService from '@/rpc/gen/TDataDepartemenService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TDataDepartemenClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TDataDepartemenService, '/api/data/departemen');
	}

	async fetch(query=null){
		return await this.client.fetch(this.stores.auth.authToken, query);
	}
	async get(departemen_id){
		return await this.client.get(this.stores.auth.authToken, departemen_id);
	}

	async create(form){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		return await this.client.create(this.stores.auth.authToken, form);
	}
	async set_name(departemen_id, new_name){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_name(this.stores.auth.authToken, departemen_id, new_name);
	}
	async set_enabled(departemen_id, new_enabled){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_enabled(this.stores.auth.authToken, departemen_id, new_enabled);
	}
}

const dataDepartemenClient = new TDataDepartemenClient();

export { TDataDepartemenClient, dataDepartemenClient }
export default dataDepartemenClient