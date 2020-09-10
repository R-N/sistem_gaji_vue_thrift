<template>
	<v-row
		align="start"
		justify="start"
	>
		<v-col
			align="start"
			justify="start"
		>
			<v-card class="fill-width">
				<vue-dropzone ref="myTableDropzone" id="dropzone" :options="dropzoneOptions" useCustomSlot @vdropzone-file-added="onTableFileDropped" class="">
					<v-card-title class="my-0 pb-0"  align="start">
						<h1>Backup </h1>
					</v-card-title>
					<v-card-title class="my-0 pt-0"  align="start">
						<v-row>
							<v-col align="start" justify="start">
		    					<v-btn icon @click.stop="createDialog = true">
		    						<v-icon size="32">mdi-plus</v-icon>
		    					</v-btn>
		    					<v-btn icon @click.stop="uploadDialog = true">
		    						<v-icon size="32">mdi-upload</v-icon>
		    					</v-btn>
		    				</v-col>
							<v-spacer></v-spacer>
		    				<v-col  align="start" justify="start">
								<v-text-field
									class="pt-0 mt-0"
									v-model="search"
									append-icon="mdi-magnify"
									label="Search"
									single-line
									hide-details
								></v-text-field>
							</v-col>
						</v-row>
					</v-card-title>
					<v-card-text>
						<v-data-table
							class="backup-table"
							:headers="headers"
							:items="backups"
							item-key="file_name"
							:search="search"
							:loading="busy"
						>
							<template v-slot:item.actions="{ item }">
		    					<v-btn icon @click.stop="downloadBackup(item)" class="">
		    						<v-icon size="32" small>mdi-download</v-icon>
		    					</v-btn>
		    					<v-btn icon @click.stop="deleteBackup(item)" class="">
		    						<v-icon size="32" small>mdi-delete</v-icon>
		    					</v-btn>
							</template>
						</v-data-table>
					</v-card-text>
				</vue-dropzone>
			</v-card>
		</v-col>
		<v-dialog
			v-model="uploadDialog"
			max-width="290"
		>
			<v-card>
				<vue-dropzone ref="myDialogDropzone" id="dropzone" :options="dropzoneOptions" useCustomSlot @vdropzone-file-added="onDialogFileDropped" class="text-left">
					<v-card-title class="headline">Upload Backup</v-card-title>
					<v-card-text>
						<p class="text-left">Pilih file backup (xlsx)</p>
		    			<v-file-input multiple ref="myFileInput" label="File input" v-model="files" @click.stop="" accept=".xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" show-size></v-file-input>
					</v-card-text>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn
							color="green darken-1"
							text
							@click.stop="uploadDialog = false"
						>
							Cancel
						</v-btn>
						<v-btn
							color="green darken-1"
							text
							@click.stop="uploadBackup"
						>
							Upload
						</v-btn>
					</v-card-actions>
				</vue-dropzone>
			</v-card>
		</v-dialog>
		<v-dialog
			v-model="createDialog"
			max-width="290"
		>
			<v-card>
				<v-card-title class="headline">Upload Backup</v-card-title>
				<v-card-text>
					<p class="text-left">Masukkan nama backup (tanpa ekstensi)</p>
					<v-text-field class="bigger-input" label="Backup Name" v-model="backupName" :disabled="busy"/>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="green darken-1"
						text
						@click.stop="createDialog = false"
					>
						Cancel
					</v-btn>
					<v-btn
						color="green darken-1"
						text
						@click.stop="createBackup"
					>
						Create
					</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</v-row>
</template>

<script>
import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import { authStore, clientStore, appStore } from "@/store/stores";
import { TAuthError, TAuthErrorCode, TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/auth_types";
import { TFileError, TFileErrorCode, T_FILE_ERROR_STR } from "@/rpc/gen/file_types";
import { router } from "@/router/index";
import axios from 'axios';
//import fileDownload from 'js-file-download';
import FileSaver from 'file-saver';
//import FileUpload from 'vue-upload-component';
import vueDropzone from 'vue2-dropzone'


@Component({
  	name: "BackupView",
  	components: {
  		vueDropzone
  	}
	//beforeRouteEnter: authRouter.routeRequireLoginNow
})
class BackupView extends BaseView {
	file = null
	files = []
	fromDrop = false
	immediateUpload = false;
	backupName = ''
	fetchingBackups = true
	uploadDialog = false;
	createDialog = false;

	search = ''
	headers = [
		{ text: 'File', value: 'file_name' },
		{ text: 'Dibuat/Terakhir Diubah', value: 'last_modified' },
        { text: 'Actions', value: 'actions', sortable: false },
	]
	backups = []

	get dropzoneOptions() {
		return {
			url: defaultBackendUrl + "/backup/upload/",
			params: this.dropzoneParams,
			maxFilesize: 1,
			clickable: false,
			uploadMultiple: false,
			autoProcessQueue: false,
			acceptedFiles: ".xlsx",
			mimeTypes: ['application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
		}
	}
	dropzoneParams(files, xhr, chunk=null){
		return {
			"upload_token": "asdasd"
		}
	}
	onFileDropped(file){		
		if(!this.file)
			this.file = file;
		else
			this.files.push(file);
		this.fromDrop = true;
	}
	onTableFileDropped(file){
		this.$refs["myTableDropzone"].removeFile(file);
		this.immediateUpload = true;
		this.onFileDropped(file);
	}
	onDialogFileDropped(file){
		this.$refs["myDialogDropzone"].removeFile(file);
		this.onFileDropped(file);
	}
	@Watch("file")
	async onFileChanged(file, old){
		if(this.fromDrop){
			if(file){
				if (!file.accepted){
					if (this.files.length == 0){
						this.fromDrop = false;
						this.file = old;
					}else{
						this.file = this.files.shift();
					}
					appStore.pushTabDialog({
						title: "Error",
						text: "Format harus xlsx"
					});
				}else if (this.immediateUpload){
					await this.uploadBackup();
					this.immediateUpload = false;
				}
			}
		}
	}
	async beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	async mounted(){
		appStore.setBreadcrumbs([
			{ text: "Beranda", disabled: false, href: "#" },
			{ text: "Beranda", disabled: false, href: "#" },
			{ text: "Beranda", disabled: false, href: "#" },
		]);
		await this.fetchBackups();
	}

	async createBackup(){
		const view = this;
		view.busy=true;
		try{
			if (!this.backupName) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			let created = await clientStore.backup.create_backup(this.backupName);
			this.backupName = '';
			view.createDialog = false;
			this.backups.push(created);
		} finally {
			view.busy = false;
		}
	}
	async deleteBackup(item){
		const view = this;
		view.busy=true;

		try{
			if (!item.file_name) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			await clientStore.backup.delete_backup(item.file_name);

	        const index = this.backups.indexOf(item);
	        this.backups.splice(index, 1);
		} catch (error) {
			if (error instanceof TFileError){
				appStore.pushTabDialog({
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
		view.fetchingBackups = true;
		try{
			this.backups = await clientStore.backup.fetch_backups();
		} finally {
			view.busy = false;
			view.fetchingBackups = false;
		}
	}
	async downloadBackup(item){
		const view = this;
		view.busy=true;
		try{
			let blob = await clientStore.backup.download_backup(item.file_name);
			FileSaver.saveAs(blob, item.file_name);
		} finally {
			view.busy = false;
		}
	}
	async uploadBackup(){
		const view = this;
		view.busy=true;
		try{
			if(!view.file && view.files.length) view.file = view.files.shift();
			while(view.file || view.files.length){
				let uploaded = await clientStore.backup.upload_backup(view.file, view.backupName);
				view.backups.push(uploaded);
				if (view.files.length){
					view.file = view.files.shift();
				}else{
					view.file = null;
				}
			}
			view.uploadDialog = false;
		} catch (error) {
			if (error instanceof TFileError){
				appStore.pushTabDialog({
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
}
export { BackupView } 
export default BackupView
</script>
<style scoped>
.backup-table{
	background: #00000000;
}
</style>
