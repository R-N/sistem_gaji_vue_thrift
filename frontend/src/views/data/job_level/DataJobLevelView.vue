<template>
	<main-card title="Job Level">
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
				:items="jobLevel"
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
			<data-job-level-form-dialog
				v-model="createDialog"
				@create="p => { jobLevel.push(p) }"
				:parent-busy="busy"
			/>
		</template>
	</main-card>
</template>

<script>
import { TUserRole, T_ROLE_STR, T_ROLE_DOUBLES } from "@/rpc/gen/user.user.types_types";
import { 
	TJobLevelError, 
	NAMA_MAX_LEN 
} from "@/rpc/gen/data.job_level.errors_types";
import { TJobLevelQuery } from '@/rpc/gen/data.job_level.structs_types';

import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAMA_RULES } from '@/lib/validators/data/job_level';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/checkbox/SyncCheckbox';
import EditableCell from '@/components/form/EditableCell';

import DataJobLevelFormDialog from '@/views/data/job_level/DataJobLevelFormDialog';

@Component({
  	name: "DataJobLevelView",
  	components: {
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		DataJobLevelFormDialog
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataJobLevelView extends BaseView {
	createDialog = false;
	search = ''
	jobLevel = []
	namaLenMax = NAMA_MAX_LEN
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
			{ text: "Job Level" },
		]);
		await this.fetchJobLevel();
	}
	async fetchJobLevel(){
		const view = this;
		view.busy = true;
		let query = new TJobLevelQuery();
		try{
			let jobLevel = await stores.client.data.jobLevel.fetch(query);
			this.jobLevel = jobLevel;
		} catch(error){
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	setNamaConfirmText(jobLevel){
		return "Apa Anda yakin ingin mengubah nama untuk job level '" 
			+ jobLevel.nama + "' menjadi '" 
			+ jobLevel.namaEdit + "'?"
	}
	async setNama(jobLevel, nama){
		const view = this;
		view.busy=true;
		try{
			await stores.client.data.jobLevel.set_nama(jobLevel.id, nama);
			jobLevel.nama = nama;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setEnabledConfirmText(jobLevel){
		let action = jobLevel.enabled ? 'menonaktifkan' : 'mengaktifkan';
		return "Apa Anda yakin ingin " + action 
			+ " job level '" + jobLevel.nama + "'?";
	}
	async setEnabled(jobLevel, enabled){
		const view = this;
		view.busy=true;
		if (enabled === undefined || enabled === null)
			enabled = !jobLevel.enabled;
		try{
			await stores.client.data.jobLevel.set_enabled(jobLevel.id, enabled);
			jobLevel.enabled = enabled;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	showError(error){
		if (stores.helper.error.showFilteredError(error, 
			[TJobLevelError]
		)) return;
		throw error;
	}
}
export { DataJobLevelView } 
export default DataJobLevelView
</script>
<style scoped>
</style>
