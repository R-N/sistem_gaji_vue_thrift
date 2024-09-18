<template>
	<main-card title="Perusahaan">
		<template v-slot:toolbar-left>
			<v-tooltip bottom>
				<template v-slot:activator="{ on, attrs }">
					<v-btn 
						icon 
						@click.stop="createDialog = true" 
						v-bind="attrs" 
						v-on="on"
						:disabled="busy"
					>
						<v-icon size="32">mdi-plus</v-icon>
					</v-btn>
				</template>
				<span>Buat</span>
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
				:disabled="busy"
			></v-text-field>
		</template>
		<template v-slot:default>
			<v-data-table
				class="backup-table"
				:headers="headers"
				:items="perusahaan"
				item-key="id"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.nama="{ item }">
					<editable-cell 
						v-if="isSuperAdmin"
						@edit="item.namaEdit = item.nama"
						@finish="setNama(item, item.namaEdit)"
						:change-detector="() => item.nama != item.namaEdit"
						:confirm-text-maker="() => setNamaConfirmText(item)"
						:parent-busy="busy"
					>
						<template v-slot:editing>
							<v-text-field 
								name="nama" 
								v-model="item.namaEdit" 
								:rules="namaRules"
								:counter="namaLenMax"
								type="text"
								:disabled="busy"
							/>
						</template>
						<template v-slot:default>
							<span>{{ item.nama }}</span>
						</template>
					</editable-cell>
					<span v-else >{{ item.nama }}</span>
				</template>
				<template v-slot:item.enabled="{ item }">
					<v-tooltip 
						v-if="isSuperAdmin"
						bottom
					>
						<template v-slot:activator="{ on, attrs }">
						    <sync-checkbox 
						    	:input-value="item.enabled" 
						    	@change="value => setEnabled(item, value)"
						    	:confirm-text-maker="() => setEnabledConfirmText(item)"
						    	readonly
						    	v-bind="attrs" v-on="on"
								:disabled="busy"
					    	/>
						</template>
						<span>{{ item.enabled ? "Nonaktifkan" : "Aktifkan" }}</span>
					</v-tooltip>
					<span v-else>
					    <v-simple-checkbox 
					    	:value="item.enabled" 
					    	disabled
				    	/>
				    </span>
				</template>
			</v-data-table>
			<data-perusahaan-form-dialog
				v-model="createDialog"
				@create="p => { perusahaan.push(p) }"
				:parent-busy="busy"
			/>
		</template>
	</main-card>
</template>

<script>
import { TUserRole, T_USER_ROLE_STR, T_USER_ROLE_DOUBLES } from "@/rpc/gen/user.user.types_types";
import { 
	TPerusahaanError, 
	NAMA_LEN_MAX 
} from "@/rpc/gen/data.perusahaan.errors_types";
import { TPerusahaanQuery } from '@/rpc/gen/data.perusahaan.structs_types';

import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAMA_RULES } from '@/lib/validators/data/perusahaan';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/form/SyncCheckbox';
import EditableCell from '@/components/form/EditableCell';

import DataPerusahaanFormDialog from '@/views/data/perusahaan/DataPerusahaanFormDialog';

@Component({
  	name: "DataPerusahaanView",
  	components: {
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		DataPerusahaanFormDialog
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataPerusahaanView extends BaseView {
	createDialog = false;
	search = ''
	perusahaan = []
	namaLenMax = NAMA_LEN_MAX
	namaRules = NAMA_RULES

	get headers(){
		let headers = [
			{ text: 'Nama', value: 'nama' },
			{ text: 'Aktif', value: 'enabled', align: 'center' }
		]
		return headers;
	}

	get isSuperAdmin(){
		return stores.auth.user.role == TUserRole.SUPER_ADMIN;
	}


	async mounted(){
		stores.app.setBreadcrumbs([
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Data" },
			{ text: "Perusahaan" },
		]);
		await this.fetchPerusahaan();
	}
	async fetchPerusahaan(){
		const view = this;
		view.busy = true;
		let query = new TPerusahaanQuery();
		try{
			let perusahaan = await stores.client.data.perusahaan.fetch(query);
        	await stores.settings.setPerusahaans(perusahaan);
			this.perusahaan = perusahaan;
		} catch(error){
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	setNamaConfirmText(perusahaan){
		return "Apa Anda yakin ingin mengubah nama untuk perusahaan '" 
			+ perusahaan.nama + "' menjadi '" 
			+ perusahaan.namaEdit + "'?"
	}
	async setNama(perusahaan, nama){
		const view = this;
		view.busy=true;
		console.log("Set nama to: " + nama);
		try{
			await stores.client.data.perusahaan.set_nama(perusahaan.id, nama);
			perusahaan.nama = nama;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setEnabledConfirmText(perusahaan){
		let action = perusahaan.enabled ? 'menonaktifkan' : 'mengaktifkan';
		return "Apa Anda yakin ingin " + action 
			+ " perusahaan '" + perusahaan.nama + "'?";
	}
	async setEnabled(perusahaan, enabled){
		const view = this;
		view.busy=true;
		if (enabled === undefined || enabled === null)
			enabled = !perusahaan.enabled;
		try{
			await stores.client.data.perusahaan.set_enabled(perusahaan.id, enabled);
			perusahaan.enabled = enabled;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	showError(error){
		if (stores.helper.error.showFilteredError(error, 
			[TPerusahaanError]
		)) return;
		throw error;
	}
}
export { DataPerusahaanView } 
export default DataPerusahaanView
</script>
<style scoped>
</style>
