import TBackupService from '@/rpc/gen/TBackupService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/auth_types';
import { TFileError, TFileErrorCode } from "@/rpc/gen/file_types";
import { TUploadError, TUploadErrorCode } from "@/rpc/gen/upload_types";
import axios from 'axios';


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
	async get_download_token(file_name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.get_download_token(this.authStore.authToken, file_name);
	}
	async download_backup(file_name){
		if (!file_name) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
		var token = await this.get_download_token(file_name);
		var response = await axios({
			method: 'post',
			url: defaultBackendUrl + "/backup/download/",
			data: { download_token: token },
			responseType: 'arraybuffer'
		});
		let blob = new Blob(
			[response.data], 
			{ type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
		);
		return blob;
	}
	async get_upload_token(file_name){
		this.clientStore.auth.requireRole(TUserRole.ADMIN_UTAMA);
		return await this.client.get_upload_token(this.authStore.authToken, file_name);
	}
	async upload_backup(file, file_name=null){
		if (!file) throw new TUploadError({ code: TUploadErrorCode.FILE_NOT_PROVIDED});
		file_name = file_name || file.name;
		if (!file_name) throw new TUploadError({ code: TUploadErrorCode.FILE_NOT_PROVIDED});
		//if (!file.accepted) throw new TUploadError({ code: TUploadErrorCode.FILE_INVALID});
		var token = await this.get_upload_token(file_name);

		const form = new FormData();
		form.append("file", file);
		form.append("upload_token", token);

		var response = await axios({
			method: 'post',
			url: defaultBackendUrl + "/backup/upload/",
			data: form,
			headers: {'Content-Type': 'multipart/form-data' },
			responseType: 'json'
		});
		return response.data;
	}
}

export { TBackupServiceClient }
export default TBackupServiceClient