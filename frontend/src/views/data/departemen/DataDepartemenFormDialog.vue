<template>
	<v-dialog
		v-model="myDialog"
		max-width="400"
		:persistent="busy"
	>
		<v-card class="">
		    <v-form ref="myForm" v-model="valid" @submit.prevent="create" class="p-2" :disabled="!interactable">
				<v-card-title class="headline">Buat Departemen</v-card-title>
				<v-card-text>
			    	<v-text-field 
			    		name="name"
			    		class="bigger-input" 
			    		label="Nama" 
			    		v-model="name" 
			    		:disabled="!interactable" 
			    		required
			    		:rules="nameRules"
						:counter="nameLenMax"
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
import { TUserRole, T_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { 
	TDepartemenError, 
	NAME_MAX_LEN 
} from "@/rpc/gen/data.departemen.errors_types";
import { TDepartemenForm } from "@/rpc/gen/data.departemen.structs_types";

import stores from "@/store/stores";
import { NAME_RULES } from '@/lib/validators/data/departemen';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "DataDepartemenFormDialog",
	components: {
		CardTitle
	}
})
class DataDepartemenFormDialog extends WorkingComponent {
	@Prop({ default: false }) disabled;
	@Model('change', { type: Boolean }) dialog;

	name = ''

	nameRules = NAME_RULES

	nameLenMax = NAME_MAX_LEN

	valid = true;

	@Watch('myDialog')
	onDialogChange(val, oldVal){
		if( this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
		this.name = ''
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

	setPerusahaan(value){
		this.perusahaan = value;
	}

	async create(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		let form = new TDepartemenForm({
			name: this.name,
			perusahaan_id: stores.settings.perusahaanId,
		});
		try{
			let departemen = await stores.client.data.departemen.create(form);
			view.$emit("create", departemen);
			view.close();
		} catch (error) {
			if (stores.helper.error.showFilteredError(error, 
				[TDepartemenError]
			)) return;
			throw error;
		} finally {
			view.busy = false;
		}
	}
}
export { DataDepartemenFormDialog }
export default DataDepartemenFormDialog
</script>

<style scoped>
</style>
