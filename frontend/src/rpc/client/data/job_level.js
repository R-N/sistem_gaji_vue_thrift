import TDataJobLevelService from '@/rpc/gen/TDataJobLevelService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TDataJobLevelClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TDataJobLevelService, '/api/data/job-level');
	}

	async fetch(query=null){
		return await this.client.fetch(this.stores.auth.authToken, query);
	}
	async get(job_level_id){
		return await this.client.get(this.stores.auth.authToken, job_level_id);
	}

	async create(form){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		return await this.client.create(this.stores.auth.authToken, form);
	}
	async set_name(job_level_id, new_name){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_name(this.stores.auth.authToken, job_level_id, new_name);
	}
	async set_enabled(job_level_id, new_enabled){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_enabled(this.stores.auth.authToken, job_level_id, new_enabled);
	}
	async set_gaji_pokok(job_level_id, new_gaji_pokok){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_gaji_pokok(this.stores.auth.authToken, job_level_id, new_gaji_pokok);
	}
	async set_tunjangan_jabatan(job_level_id, new_tunjangan_jabatan){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_tunjangan_jabatan(this.stores.auth.authToken, job_level_id, new_tunjangan_jabatan);
	}
	async set_upah_lembur(job_level_id, new_upah_lembur, i){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_upah_lembur(this.stores.auth.authToken, job_level_id, new_upah_lembur, i);
	}
	async set_upah_lembur_1(job_level_id, new_upah_lembur){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_upah_lembur_1(this.stores.auth.authToken, job_level_id, new_upah_lembur);
	}
	async set_upah_lembur_2(job_level_id, new_upah_lembur){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_upah_lembur_2(this.stores.auth.authToken, job_level_id, new_upah_lembur);
	}
	async set_upah_lembur_3(job_level_id, new_upah_lembur){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_upah_lembur_3(this.stores.auth.authToken, job_level_id, new_upah_lembur);
	}
}

const dataJobLevelClient = new TDataJobLevelClient();

export { TDataJobLevelClient, dataJobLevelClient }
export default dataJobLevelClient