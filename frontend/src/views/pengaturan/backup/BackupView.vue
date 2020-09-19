<template>
	<main-card title="Backup">
		<template v-slot:toolbar-left>
			<v-tooltip bottom>
				<template v-slot:activator="{ on, attrs }">
					<v-btn icon @click.stop="createDialog = true" v-bind="attrs" v-on="on">
						<v-icon size="32">mdi-plus</v-icon>
					</v-btn>
				</template>
				<span>Buat</span>
			</v-tooltip>
			<v-tooltip bottom>
				<template v-slot:activator="{ on, attrs }">
					<v-btn icon @click.stop="uploadDialog = true" v-on="on">
						<v-icon size="32">mdi-upload</v-icon>
					</v-btn>
				</template>
				<span>Upload</span>
			</v-tooltip>
		</template>
		<template v-slot:toolbar-right>
			<v-text-field
				class="pt-0 mt-0"
				v-model="search"
				append-icon="mdi-magnify"
				label="Search"
				single-line
				hide-details
			></v-text-field>
		</template>
		<template v-slot:default>
			<v-data-table
				class="backup-table"
				:headers="headers"
				:items="backups"
				item-key="file_name"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.actions="{ item }">
					<v-tooltip bottom>
						<template v-slot:activator="{ on, attrs }">
							<v-btn icon @click.stop="downloadBackup(item)" class="" v-bind="attrs" v-on="on">
								<v-icon size="32" small>mdi-download</v-icon>
							</v-btn>
						</template>
						<span>Download</span>
					</v-tooltip>
					<v-tooltip bottom>
						<template v-slot:activator="{ on, attrs }">
							<v-btn icon @click.stop="prepareDeleteBackup(item)" class="" v-bind="attrs" v-on="on">
								<v-icon size="32" small>mdi-delete</v-icon>
							</v-btn>
						</template>
						<span>Hapus</span>
					</v-tooltip>
				</template>
			</v-data-table>
			<file-upload-dialog 
				v-model="uploadDialog" 
				:on-upload="uploadBackup" 
				title="Upload Backup"
				text="Silahkan pilih file backup untuk diupload (xlsx)"
				label="File backup"
			/>
			<simple-input-dialog 
				v-model="createDialog" 
				:on-confirm="createBackup"
				title="Buat Backup"
				text="Silahkan masukkan nama backup"
				label="Nama backup" 
			/>
			<simple-input-dialog 
				v-model="deleteDialog" 
				:on-confirm="onConfirmDelete"
				title="Hapus Backup"
				:text="deleteText"
				no-input="true"
			/>
		</template>
	</main-card>
</template>

<script>
import axios from 'axios';
import FileSaver from 'file-saver';

import { TAuthError, TAuthErrorCode } from "@/rpc/gen/user.auth.errors_types";
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { TFileError, TFileErrorCode, T_FILE_ERROR_STR } from "@/rpc/gen/file.file.errors_types";


import stores from "@/store/stores";
import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import FileUploadDialog from '@/components/dialog/FileUploadDialog'
import SimpleInputDialog from '@/components/dialog/SimpleInputDialog'
import MainCard from '@/components/card/MainCard';


@Component({
  	name: "BackupView",
  	components: {
  		FileUploadDialog,
  		SimpleInputDialog,
  		MainCard
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.ADMIN_UTAMA)
})
class BackupView extends BaseView {
	uploadDialog = false;
	createDialog = false;
	toDelete = null;
	get deleteDialog(){
		return !!this.toDelete;
	}
	set deleteDialog(value){
		if(!value) this.toDelete = null;
	}

	search = ''
	headers = [
		{ text: 'File', value: 'file_name' },
		{ text: 'Dibuat/Terakhir Diubah', value: 'last_modified' },
        { text: 'Actions', value: 'actions', sortable: false },
	]
	backups = []

	async beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	async mounted(){
		stores.app.setBreadcrumbs([
			{ text: "Beranda", disabled: false, to: { name: "beranda" }, exact: true },
			{ text: "Pengaturan", disabled: true },
			{ text: "Backup", disabled: true },
		]);
		await this.fetchBackups();
	}

	async createBackup(file_name){
		const view = this;
		view.busy=true;
		try{
			if (!file_name) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			let created = await stores.client.system.backup.create_backup(file_name);
			this.backupName = '';
			//view.createDialog = false;
			this.backups.push(created);
		} catch (error) {
			if (error instanceof TFileError){
				stores.app.pushTabDialog({
					title: "Error",
					text: T_FILE_ERROR_STR[error.code]
				});
			}else{
				throw error;
			}
		} finally {
			view.busy = false;
		}
	}
	prepareDeleteBackup(item){
		this.toDelete = item;
		//this.deleteDialog = true;
	}
	get deleteText(){
		if (!this.toDelete) return '';
		return "Apa Anda yakin ingin menghapus backup '" + this.toDelete.file_name + "'?";
	}
	async onConfirmDelete(){
		const item = this.toDelete;
		await this.deleteBackup(item);
		this.toDelete = null;
	}
	async deleteBackup(item){
		const view = this;
		view.busy=true;
		try{
			if (!item.file_name) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			await stores.client.system.backup.delete_backup(item.file_name);

	        const index = this.backups.indexOf(item);
	        this.backups.splice(index, 1);
		} catch (error) {
			if (error instanceof TFileError){
				stores.app.pushTabDialog({
					title: "Error",
					text: T_FILE_ERROR_STR[error.code]
				});
			}else{
				throw error;
			}
		} finally {
			view.busy = false;
		}
	}
	async fetchBackups(){
		const view = this;
		view.busy = true;
		try{
			this.backups = await stores.client.system.backup.fetch_backups();
		} finally {
			view.busy = false;
		}
	}
	async downloadBackup(item){
		const view = this;
		view.busy=true;
		try{
			let blob = await stores.client.system.backup.download_backup(item.file_name);
			FileSaver.saveAs(blob, item.file_name);
		} finally {
			view.busy = false;
		}
	}
	async uploadBackup(file){
		let uploaded = await stores.client.system.backup.upload_backup(file);
		this.backups.push(uploaded);
	}
}
export { BackupView } 
export default BackupView
</script>
<style scoped>
.backup-table{
	background: #00000000;
}
</style>
