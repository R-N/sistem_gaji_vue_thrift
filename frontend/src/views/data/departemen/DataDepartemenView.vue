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
				<template v-slot:item.name="{ item }">
					<editable-cell 
						v-if="isSuperAdmin"
						@edit="item.nameEdit = item.name"
						@finish="setName(item, item.nameEdit)"
						:change-detector="() => item.name != item.nameEdit"
						:confirm-text-maker="() => setNameConfirmText(item)"
						:parent-busy="busy"
					>
						<template v-slot:editing>
							<v-text-field 
								name="name" 
								v-model="item.nameEdit" 
								:rules="nameRules"
								:counter="nameLenMax"
								type="text"
								:disabled="busy"
							/>
						</template>
						<template v-slot:default>
							<span>{{ item.name }}</span>
						</template>
					</editable-cell>
					<span v-else >{{ item.name }}</span>
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
import { TUserRole, T_ROLE_STR, T_ROLE_DOUBLES } from "@/rpc/gen/user.user.types_types";
import { 
	TDepartemenError, 
	NAME_MAX_LEN 
} from "@/rpc/gen/data.departemen.errors_types";
import { TDepartemenQuery } from '@/rpc/gen/data.departemen.structs_types';

import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAME_RULES } from '@/lib/validators/data/departemen';

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
	nameLenMax = NAME_MAX_LEN
	nameRules = NAME_RULES

	get headers(){
		let headers = [
			{ text: 'Nama', value: 'name' },
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
	setNameConfirmText(departemen){
		return "Apa Anda yakin ingin mengubah name untuk departemen '" 
			+ departemen.name + "' menjadi '" 
			+ departemen.nameEdit + "'?"
	}
	async setName(departemen, name){
		const view = this;
		view.busy=true;
		try{
			await stores.client.data.departemen.set_name(departemen.id, name);
			departemen.name = name;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setEnabledConfirmText(departemen){
		let action = departemen.enabled ? 'menonaktifkan' : 'mengaktifkan';
		return "Apa Anda yakin ingin " + action 
			+ " departemen '" + departemen.name + "'?";
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
