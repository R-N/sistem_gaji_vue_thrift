<template>
	<base-crud-view 
		title="Departemen"
		:create="() => createDialog=true"
		:fetch="fetch"
		create-text="Buat Akun"
		v-model:search="search"
	>
		<template v-slot:default>
			<v-data-table
				class="backup-table"
				:headers="headers"
				:items="items"
				item-key="id"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.name="{ item }">
					<editable-cell-text-field
						name="name"
						:counter="nameMaxLen"
						:confirm-text-maker="(value) => setFieldConfirmText('name', item, value)"
						:value="item.name" 
						:on-finish="(value) => setName(item, value)"
						:rules="nameRules"
						:disabled="!isSuperAdmin || busy"
					/>
				</template>
				<template v-slot:item.enabled="{ item }">
					<sync-checkbox 
						:input-value="item.enabled" 
						:on-change="value => setEnabled(item, value)"
						:confirm-text-maker="() => setEnabledConfirmText(item)"
						readonly
						textDisable="Nonaktifkan"
						textEnable="Aktifkan"
						:disabled="!isSuperAdmin || busy"
					/>
				</template>
			</v-data-table>
			<data-departemen-form-dialog
				v-model="createDialog"
				@create="addItem"
				:parent-busy="busy"
			/>
		</template>
	</base-crud-view>
</template>

<script>
import { TUserRole } from "@/rpc/gen/user.user.types_types";
import { 
	TDepartemenError, 
	NAME_MAX_LEN 
} from "@/rpc/gen/data.departemen.errors_types";
import { TDepartemenQuery } from '@/rpc/gen/data.departemen.structs_types';

import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAME_RULES } from '@/lib/validators/data/departemen';

import { Component } from 'vue-property-decorator';

import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/checkbox/SyncCheckbox';

import DataDepartemenFormDialog from '@/views/data/departemen/DataDepartemenFormDialog';
import { BaseCrudView } from '@/views/BaseCrudView';
import { BaseCrudViewBase } from '@/views/BaseCrudViewBase';
import EditableCellTextField from '@/components/form/editable_cell/EditableCellTextField';

@Component({
  	name: "DataDepartemenView",
  	components: {
  		MainCard,
  		SyncCheckbox,
  		DataDepartemenFormDialog,
		BaseCrudView,
		EditableCellTextField
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataDepartemenView extends BaseCrudViewBase {
	createDialog = false;
	nameMaxLen = NAME_MAX_LEN
	nameRules = NAME_RULES

	get nameField(){ return "name"; }
    get itemName(){ return 'Departemen'; }
    get client(){ return stores.client.data.departemen; }
    get query(){ return new TDepartemenQuery(); }
	get breadcrumbs(){
		return [
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Data" },
			{ text: "Departemen" },
		]
	}
	get headers(){
		let headers = [
			{ text: 'Nama', value: 'name' },
			{ text: 'Aktif', value: 'enabled', align: 'center' }
		]
		return headers;
	}
	get filteredErrors() { return [TDepartemenError]; }
}
export { DataDepartemenView } 
export default DataDepartemenView
</script>
<style scoped>
</style>
