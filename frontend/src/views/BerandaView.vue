<template>
	<v-main v-if="isLoggedIn">
		<v-container
			class="fill-height"
			fluid
		>
			<v-row
				align="center"
				justify="center"
				class="flex-column"
			>
				<v-text-field class="bigger-input" label="Backup Name" v-model="backupName" :disabled="busy"/>
		    	<v-btn raised color="primary" class="text-center mx-0" @click="createBackup" :loading="busy">Backup</v-btn>
		    	<v-btn raised color="primary" class="text-center mx-0" @click="fetchBackups" :loading="busy">Fetch Backups</v-btn>
		    	<v-btn raised color="primary" class="text-center mx-0" @click="downloadBackup" :loading="busy">Download Backup</v-btn>
		    	<v-btn raised color="primary" class="text-center mx-0" @click="hello" :loading="busy">Hello Admin Utama</v-btn>
		        <h4 class="text-center mb-4" v-if="msg">{{ msg }}</h4>
			</v-row>
		</v-container>
	</v-main>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import { authStore, clientStore, appStore } from "@/store/stores";
import { TAuthError, TAuthErrorCode, TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/auth_types";
import { TFileError, TFileErrorCode, T_FILE_ERROR_STR } from "@/rpc/gen/file_types";
import { router } from "@/router/index";
import axios from 'axios';
//import fileDownload from 'js-file-download';
import FileSaver from 'file-saver';

@Component({
  	name: "BerandaView",
	//beforeRouteEnter: authRouter.routeRequireLoginNow
})
class BerandaView extends BaseView {
	backupName = ''
	msg = ''

	beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	
	async hello(){
		const view = this;
		view.busy=true;
		try{
			this.msg = await clientStore.hello.hello_admin_utama();
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.INVALID_ROLE){
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
			if (error instanceof TAuthError && error.code === TAuthErrorCode.INVALID_ROLE){
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
			if (error instanceof TAuthError && error.code === TAuthErrorCode.INVALID_ROLE){
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
			if (!this.backupName) throw new TFileError({ code: TFileErrorCode.FILE_NAME_EMPTY});
			var token = await clientStore.backup.download_backup(this.backupName);

			try{
				var response = await axios({
					method: 'post',
					url: defaultBackendUrl + "/download/",
					data: {
						download_token: token
					},
					responseType: 'arraybuffer'
				});
				let blob = new Blob(
					[response.data], 
					{ 
						type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
					}
				);
				FileSaver.saveAs(blob, this.backupName);
			}catch(error){
				console.log(error);
				console.log(error.response);
			}
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.INVALID_ROLE){
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
}
export { BerandaView } 
export default BerandaView
</script>

<style scoped>

</style>
