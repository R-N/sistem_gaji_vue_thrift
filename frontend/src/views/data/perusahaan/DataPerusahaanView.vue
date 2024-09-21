<template>
	<base-crud-view 
		title="Perusahaan"
		:create="() => createDialog=true"
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
				<template v-slot:item.nama="{ item }">
					<editable-cell-text-field
						name="nama"
						:counter="namaLenMax"
						:confirm-text-maker="(value) => setFieldConfirmText('nama', item, value)"
						:value="item.nama" 
						@change="(value) => setNama(item, value)"
						:rules="namaRules"
						:disabled="!isSuperAdmin || busy"
					/>
				</template>
				<template v-slot:item.enabled="{ item }">
					<sync-checkbox 
						:input-value="item.enabled" 
						@change="value => setEnabled(item, value)"
						:confirm-text-maker="() => setEnabledConfirmText(item)"
						readonly
						textDisable="Nonaktifkan"
						textEnable="Aktifkan"
						:disabled="!isSuperAdmin || busy"
					/>
				</template>
			</v-data-table>
			<data-perusahaan-form-dialog
				v-model="createDialog"
				@create="addItem"
				:parent-busy="busy"
			/>
		</template>
	</base-crud-view>
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
import SyncCheckbox from '@/components/checkbox/SyncCheckbox';
import EditableCell from '@/components/form/EditableCell';

import DataPerusahaanFormDialog from '@/views/data/perusahaan/DataPerusahaanFormDialog';
import { BaseCrudView } from '@/views/BaseCrudView';
import { BaseCrudViewBase } from '@/views/BaseCrudViewBase';
import EditableCellTextField from '@/components/form/editable_cell/EditableCellTextField';

@Component({
  	name: "DataPerusahaanView",
  	components: {
  		MainCard,
  		SyncCheckbox,
  		DataPerusahaanFormDialog,
		BaseCrudView,
		EditableCellTextField
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataPerusahaanView extends BaseCrudViewBase {
	createDialog = false;
	namaLenMax = NAMA_LEN_MAX
	namaRules = NAMA_RULES

	get nameField(){ return "nama"; }
    get itemNameLower(){ return 'perusahaan'; }
    get client(){ return stores.client.data.perusahaan; }
    get query(){ return new TPerusahaanQuery(); }
	get breadcrumbs(){
		return [
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Data" },
			{ text: "Perusahaan" },
		]
	}
	get headers(){
		let headers = [
			{ text: 'Nama', value: 'nama' },
			{ text: 'Aktif', value: 'enabled', align: 'center' }
		]
		return headers;
	}
	get filteredErrors() { return [TPerusahaanError]; }
}
export { DataPerusahaanView } 
export default DataPerusahaanView
</script>
<style scoped>
</style>
