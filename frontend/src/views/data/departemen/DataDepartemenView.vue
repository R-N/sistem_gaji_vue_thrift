<template>
	<main-card title="Departemen">
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
				:items="departemen"
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
			<data-departemen-form-dialog
				v-model="createDialog"
				@create="p => { departemen.push(p) }"
				:parent-busy="busy"
			/>
		</template>
	</main-card>
</template>

<script>
import { TUserRole, T_USER_ROLE_STR, T_USER_ROLE_DOUBLES } from "@/rpc/gen/user.user.types_types";
import { 
	TDepartemenError, 
	NAMA_LEN_MAX 
} from "@/rpc/gen/data.departemen.errors_types";
import { TDepartemenQuery } from '@/rpc/gen/data.departemen.structs_types';

import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAMA_RULES } from '@/lib/validators/data/departemen';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/checkbox/SyncCheckbox';
import EditableCell from '@/components/form/EditableCell';

import DataDepartemenFormDialog from '@/views/data/departemen/DataDepartemenFormDialog';

@Component({
  	name: "DataDepartemenView",
  	components: {
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		DataDepartemenFormDialog
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataDepartemenView extends BaseView {
	createDialog = false;
	search = ''
	departemen = []
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
			{ text: "Departemen" },
		]);
		await this.fetchDepartemen();
	}
	async fetchDepartemen(){
		const view = this;
		view.busy = true;
		let query = new TDepartemenQuery({
			perusahaan_id: stores.settings.perusahaanId
		});
		try{
			let departemen = await stores.client.data.departemen.fetch(query);
			this.departemen = departemen;
		} catch(error){
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	setNamaConfirmText(departemen){
		return "Apa Anda yakin ingin mengubah nama untuk departemen '" 
			+ departemen.nama + "' menjadi '" 
			+ departemen.namaEdit + "'?"
	}
	async setNama(departemen, nama){
		const view = this;
		view.busy=true;
		console.log("Set nama to: " + nama);
		try{
			await stores.client.data.departemen.set_nama(departemen.id, nama);
			departemen.nama = nama;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setEnabledConfirmText(departemen){
		let action = departemen.enabled ? 'menonaktifkan' : 'mengaktifkan';
		return "Apa Anda yakin ingin " + action 
			+ " departemen '" + departemen.nama + "'?";
	}
	async setEnabled(departemen, enabled){
		const view = this;
		view.busy=true;
		if (enabled === undefined || enabled === null)
			enabled = !departemen.enabled;
		try{
			await stores.client.data.departemen.set_enabled(departemen.id, enabled);
			departemen.enabled = enabled;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	showError(error){
		if (stores.helper.error.showFilteredError(error, 
			[TDepartemenError]
		)) return;
		throw error;
	}
}
export { DataDepartemenView } 
export default DataDepartemenView
</script>
<style scoped>
</style>
