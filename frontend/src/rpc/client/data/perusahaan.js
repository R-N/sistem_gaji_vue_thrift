import TDataPerusahaanService from '@/rpc/gen/TDataPerusahaanService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TDataPerusahaanClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TDataPerusahaanService, '/api/data/perusahaan');
	}

	async fetch(query=null){
		return await this.client.fetch(this.stores.auth.authToken, query);
	}
	async get(perusahaan_id){
		return await this.client.get(this.stores.auth.authToken, perusahaan_id);
	}

	async create(form){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		return await this.client.create(this.stores.auth.authToken, form);
	}
	async set_nama(perusahaan_id, new_nama){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_nama(this.stores.auth.authToken, perusahaan_id, new_nama);
	}
	async set_enabled(perusahaan_id, new_enabled){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_enabled(this.stores.auth.authToken, perusahaan_id, new_enabled);
	}
}

const dataPerusahaanClient = new TDataPerusahaanClient();

export { TDataPerusahaanClient, dataPerusahaanClient }
export default dataPerusahaanClient