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
	    					<v-btn icon @click.stop="prepareDeleteBackup(item)" class="">
	    						<v-icon size="32" small>mdi-delete</v-icon>
	    					</v-btn>
						</template>
					</v-data-table>
				</v-card-text>
			</v-card>
		</v-col>
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
import FileUploadDialog from '@/components/FileUploadDialog'
import SimpleInputDialog from '@/components/SimpleInputDialog'


@Component({
  	name: "BackupView",
  	components: {
  		FileUploadDialog,
  		SimpleInputDialog
  	}
	//beforeRouteEnter: authRouter.routeRequireLoginNow
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
		appStore.setBreadcrumbs([
			{ text: "Beranda", disabled: false, href: "#" },
			{ text: "Beranda", disabled: false, href: "#" },
			{ text: "Beranda", disabled: false, href: "#" },
		]);
	}

}
export { BackupView } 
export default BackupView
</script>
<style scoped>
</style>
