import TBackupService from '@/rpc/gen/TBackupService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/auth_types';


class TBackupServiceClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TBackupService, '/api/system/backup');
		return this;
	}

	async fetch_backups(){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.fetch_backups(this.authStore.authToken);
	}
	async create_backup(name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.create_backup(this.authStore.authToken, name);
	}
	async delete_backup(file_name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.delete_backup(this.authStore.authToken, file_name);
	}
	async download_backup(file_name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.download_backup(this.authStore.authToken, file_name);
	}
	async get_upload_token(file_name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.get_upload_token(this.authStore.authToken);
	}
}

export { TBackupServiceClient }
export default TBackupServiceClient