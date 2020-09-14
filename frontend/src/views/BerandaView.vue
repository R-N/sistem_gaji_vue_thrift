<template>
	<v-container
		class="fill-height"
		fluid
	>
		<v-row
			align="center"
			justify="center"
			class="flex-column"
		>
			<vue-dropzone ref="myDropzone" id="dropzone" :options="dropzoneOptions" useCustomSlot @vdropzone-file-added="onFileDropped">
				<div @click.stop="" class="d-flex flex-column">
			    	<v-btn raised color="primary" class="text-center mx-0" @click="fetchBackups" :disabled="busy">Fetch Backups</v-btn>
					<v-text-field class="bigger-input" label="Backup Name" v-model="backupName" :disabled="busy"/>
			    	<v-btn raised color="primary" class="text-center mx-0" @click="createBackup" :disabled="busy">Backup</v-btn>
			    	<v-btn raised color="primary" class="text-center mx-0" @click="downloadBackup" :disabled="busy">Download Backup</v-btn>
			    	<v-btn raised color="primary" class="text-center mx-0" @click="deleteBackup" :disabled="busy">Delete Backup</v-btn>
			    	<v-btn raised color="primary" class="text-center mx-0" @click="hello" :disabled="busy">Hello Admin Utama</v-btn>
			    	<v-file-input ref="myFileInput" label="File input" v-model="file" @click.stop="" accept=".xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" show-size></v-file-input>
			    	<v-btn raised color="primary" class="text-center mx-0" @click="uploadBackup" :disabled="busy">Upload</v-btn>
			        <h4 class="text-center mb-4" v-if="msg">{{ msg }}</h4>
		        </div>
			</vue-dropzone>
		</v-row>
	</v-container>
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
  	name: "BerandaView",
  	components: {
  		vueDropzone
  	}
	//beforeRouteEnter: authRouter.routeRequireLoginNow
})
class BerandaView extends BaseView {
	backupName = ''
	msg = ''
	file = null
	fromDrop = false

	get dropzoneOptions() {
		return {
			url: defaultBackendUrl + "/upload/",
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
		this.$refs["myDropzone"].removeAllFiles();
		/*
		if(this.file != null){
			appStore.pushTabDialog({
				title: "Error",
				text: "Anda hanya dapat upload 1 file"
			});
		}else{*/
			this.file = file
			this.fromDrop = true;
		//}
	}
	@Watch("file")
	onFileChanged(file, old){
		if(this.fromDrop){
			this.fromDrop = false;
			if(file && !file.accepted){
				this.file = old;
				appStore.pushTabDialog({
					title: "Error",
					text: "Format harus xlsx"
				});
			}
		}
	}
	beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	mounted(){
		appStore.setBreadcrumbs([
			{ text: "Beranda" },
		]);
	}

	async hello(){
		const view = this;
		view.busy=true;
		try{
			this.msg = await clientStore.hello.hello_admin_utama();
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else{
				console.log(error);
			}
		} finally {
			view.busy = false;
		}
	}

	async createBackup(){
		const view = this;
		view.busy=true;
		try{
			if (!this.backupName) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			await clientStore.backup.create_backup(this.backupName);
			this.msg = "Backup berhasil dibuat!";
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else if (error instanceof TFileError){
				this.msg = T_FILE_ERROR_STR[error.code];
			}else{
				throw error;
			}
		} finally {
			view.busy = false;
		}
	}
	async deleteBackup(){
		const view = this;
		view.busy=true;
		try{
			if (!this.backupName) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			await clientStore.backup.delete_backup(this.backupName);
			this.msg = "Backup " + this.backupName + " berhasil dihapus!";
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else if (error instanceof TFileError){
				this.msg = T_FILE_ERROR_STR[error.code];
			}else{
				throw error;
			}
		} finally {
			view.busy = false;
		}
	}
	async fetchBackups(){
		const view = this;
		view.busy=true;
		try{
			var backups = await clientStore.backup.fetch_backups();
			this.msg = backups.join(", ");
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else{
				throw error;
			}
		} finally {
			view.busy = false;
		}
	}
	async downloadBackup(){
		const view = this;
		view.busy=true;
		try{
			let blob = await clientStore.backup.download_backup(this.backupName);
			FileSaver.saveAs(blob, this.backupName);
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else if (error instanceof TFileError){
				this.msg = T_FILE_ERROR_STR[error.code];
			}else{
				console.log(error);
				console.log(error.response);
			}
		} finally {
			view.busy = false;
		}
	}
	async uploadBackup(){
		const view = this;
		view.busy=true;
		try{
			let uploadedName = await clientStore.backup.upload_backup(this.file, this.backupName);
			this.file = null;
			this.msg = "Berhasil upload " + uploadedName + "!";
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.ROLE_INVALID){
				this.msg = "Anda bukan " + T_USER_ROLE_STR[TUserRole.ADMIN_UTAMA] + "!";
			}else if (error instanceof TFileError){
				this.msg = T_FILE_ERROR_STR[error.code];
			}else{
				console.log(error);
				console.log(error.response);
			}
		} finally {
			view.busy = false;
		}
	}
}
export { BerandaView } 
export default BerandaView
</script>

<style scoped>

</style>
