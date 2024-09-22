<template>
	<form-dialog
		max-width="400"
		:parent-busy="busy"
		:on-submit="create"
		title="Buat Departemen"
		:disabled="disabled"
		:on-reset="reset"
		v-model="myDialog"
	>
        <template v-slot:fields="{ interactable, busy }">
			<input name="perusahaan_id" type="hidden" :value="perusahaanId" >
			<v-text-field 
				name="name"
				class="bigger-input" 
				label="Nama" 
				v-model="name" 
				:disabled="!interactable" 
				required
				:rules="nameRules"
				:counter="nameMaxLen"
			/>
		</template>
	</form-dialog>
</template>

<script>
import { 
	TDepartemenError, 
	NAME_MAX_LEN 
} from "@/rpc/gen/data.departemen.errors_types";
import { TDepartemenForm } from "@/rpc/gen/data.departemen.structs_types";

import stores from "@/store/stores";
import { NAME_RULES } from '@/lib/validators/data/departemen';

import { Component, Prop } from 'vue-property-decorator';
import { FormDialog } from '@/components/form/FormDialog'
import { FormDialogBase } from '@/components/form/FormDialogBase'

@Component({
	name: "DataDepartemenFormDialog",
	components: {
		FormDialog
	}
})
class DataDepartemenFormDialog extends FormDialogBase {
	@Prop({ default: false }) disabled;
	name = ''

	nameRules = NAME_RULES

	nameMaxLen = NAME_MAX_LEN

	valid = true;

	reset(){
		this.name = ''
	}

	async create(){
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		let form = new TDepartemenForm({
			name: this.name,
			perusahaan_id: this.perusahaanId,
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
