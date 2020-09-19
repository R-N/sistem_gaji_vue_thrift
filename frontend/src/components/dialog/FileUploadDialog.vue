<template>
	<v-dialog
		v-model="myDialog"
		max-width="290"
		:persistent="busy"
	>
		<v-card>
			<v-form @submit.prevent.stop="uploadFile">
				<vue-dropzone ref="myDialogDropzone" id="dropzone" :options="dropzoneOptions" useCustomSlot @vdropzone-file-added="onDialogFileDropped" class="text-left">
					<v-card-title class="headline">{{ title }}</v-card-title>
					<v-card-text>
						<p class="text-left">{{ text }}</p>
		    			<v-file-input multiple ref="myFileInput" :label="label" v-model="files" @click.stop="" accept=".xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" show-size></v-file-input>
					</v-card-text>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn
							color="green darken-1"
							text
							@click.stop="close()"
							:disabled="interactable"
						>
							Batal
						</v-btn>
						<v-btn
							color="green darken-1"
							text
							type="submit"
							:disabled="interactable"
							:loading="busy"
						>
							Upload
						</v-btn>
					</v-card-actions>
				</vue-dropzone>
			</v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import { appStore } from "@/store/stores";
import vueDropzone from 'vue2-dropzone'

import { TAuthError, TAuthErrorCode } from "@/rpc/gen/user.auth.errors_types";
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { TFileError, TFileErrorCode, T_FILE_ERROR_STR } from "@/rpc/gen/file.file.errors_types";
import { TUploadError, TUploadErrorCode, T_UPLOAD_ERROR_STR } from "@/rpc/gen/file.upload.errors_types";

import { emptyArray } from '@/lib/util';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';


@Component({
  	name: "FileUploadDialog",
  	components: {
  		vueDropzone
  	}
})
class FileUploadDialog extends WorkingComponent {
	@Prop(Function) preUpload;
	@Prop(Function) onUpload;
	@Prop(Function) postUpload;

	@Prop({ default: "Upload File" }) title;
	@Prop({ default: "Silahkan pilih file untuk diupload" }) text;
	@Prop({ default: "File" }) label;
	@Model('change', { type: Boolean }) dialog;
	@Prop({ default: true }) dropUpload;

	file = null
	files = []
	fromDrop = false
	immediateUpload = false;

	get interactable(){
		return this.busy || !this.dialog;
	}

	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.file = null;
			emptyArray(this.files);
			this.busy = false;
		}
		this.$emit('change', value);
	}
	close(){
		this.myDialog = false;
	}

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
		if(!this.file)
			this.file = file;
		else
			this.files.push(file);
		this.fromDrop = true;
	}
	onDialogFileDropped(file){
		this.$refs["myDialogDropzone"].removeFile(file);
		this.immediateUpload = this.dropUpload;
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
					await this.uploadFile();
					this.immediateUpload = false;
				}
			}
		}
	}

	async uploadFile(){
		const comp = this;
		comp.busy=true;
		if (comp.preUpload) comp.preUpload();
		try{
			if(!comp.file && comp.files.length) comp.file = comp.files.shift();
			while(comp.file || comp.files.length){
				await comp.onUpload(comp.file);
				if (comp.files.length){
					comp.file = comp.files.shift();
				}else{
					comp.file = null;
				}
			}
			comp.close();
		} catch (error) {
			comp.files.unshift(comp.file);
			comp.file = null;
			if (error instanceof TFileError){
				appStore.pushTabDialog({
					title: "Error",
					text: T_FILE_ERROR_STR[error.code]
				});
			} else if (error instanceof TUploadError){
				appStore.pushTabDialog({
					title: "Error",
					text: T_UPLOAD_ERROR_STR[error.code]
				});
			}else{
				throw error;
			}
		} finally {
			if (comp.postUpload) comp.postUpload();
			comp.busy = false;
		}
	}
}
export { FileUploadDialog } 
export default FileUploadDialog
</script>
<style scoped>
</style>
