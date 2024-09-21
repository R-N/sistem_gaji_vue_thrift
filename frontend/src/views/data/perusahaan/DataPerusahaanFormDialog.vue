<template>
	<form-dialog
		max-width="400"
		:parent-busy="busy"
		@submit="create"
		title="Buat Perusahaan"
		:disabled="disabled"
		:reset="reset"
		v-model="myDialog"
	>
        <template v-slot:fields="{ interactable, busy }">
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
		</template>
	</form-dialog>
</template>

<script>
import { 
	TPerusahaanError, 
	NAMA_MAX_LEN 
} from "@/rpc/gen/data.perusahaan.errors_types";
import { TPerusahaanForm } from "@/rpc/gen/data.perusahaan.structs_types";

import stores from "@/store/stores";
import { NAMA_RULES } from '@/lib/validators/data/perusahaan';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { FormDialog } from '@/components/form/FormDialog'
import { FormDialogBase } from '@/components/form/FormDialogBase'

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "DataPerusahaanFormDialog",
	components: {
		FormDialog
	}
})
class DataPerusahaanFormDialog extends FormDialogBase {
	@Prop({ default: false }) disabled;
	nama = ''

	namaRules = NAMA_RULES

	namaLenMax = NAMA_MAX_LEN

	valid = true;

	reset(){
		this.nama = ''
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
