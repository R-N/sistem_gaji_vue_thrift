<template>
	<v-dialog
		v-model="myDialog"
		max-width="400"
		:persistent="busy"
	>
		<v-card class="">
		    <v-form ref="myForm" v-model="valid" @submit.prevent="create" class="p-2" :disabled="!interactable">
				<v-card-title class="headline">Buat Perusahaan</v-card-title>
				<v-card-text>
			    	<v-text-field 
			    		name="nama"
			    		class="bigger-input" 
			    		label="Nama" 
			    		v-model="nama" 
			    		:disabled="!interactable" 
			    		required
			    		:rules="namaRules"
						:counter="namaLenMax"
		    		/>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn
							color="green darken-1"
							text
							@click.stop="close()"
							:disabled="!interactable"
						>
							Batal
						</v-btn>
						<v-btn
							type="submit"
							color="green darken-1"
							text
							:disabled="!interactable"
							:loading="busy"
						>
							Ok
						</v-btn>
					</v-card-actions>
				</v-card-text>
		    </v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { 
	TPerusahaanError, 
	NAMA_LEN_MAX 
} from "@/rpc/gen/data.perusahaan.errors_types";
import { TPerusahaanForm } from "@/rpc/gen/data.perusahaan.structs_types";

import stores from "@/store/stores";
import { NAMA_RULES } from '@/lib/validators/data/perusahaan';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "DataPerusahaanFormDialog",
	components: {
		CardTitle
	}
})
class DataPerusahaanFormDialog extends WorkingComponent {
	@Prop({ default: false }) disabled;
	@Model('change', { type: Boolean }) dialog;
	nama = ''

	namaRules = NAMA_RULES

	namaLenMax = NAMA_LEN_MAX

	valid = true;

	@Watch('myDialog')
	onDialogChange(val, oldVal){
		if( this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
		this.nama = ''
	}

	close(){
		this.busy = false;
		this.myDialog = false;
	}

	get interactable(){
		return !this.disabled && !this.busy;
	}

	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.busy = false;
		}
		this.$emit('change', value);
	}

	async create(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		let form = new TPerusahaanForm({
			nama: this.nama
		});
		try{
			let perusahaan = await stores.client.data.perusahaan.create(form);
			view.$emit("create", perusahaan);
			view.close();
		} catch (error) {
			if (stores.helper.error.showFilteredError(error, 
				[TPerusahaanError]
			)) return;
			throw error;
		} finally {
			view.busy = false;
		}
	}
}
export { DataPerusahaanFormDialog }
export default DataPerusahaanFormDialog
</script>

<style scoped>
</style>
