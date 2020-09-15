<template>
	<main-card title="Akun">
		<template v-slot:toolbar-left>
			<v-btn icon @click.stop="createDialog = true">
				<v-icon size="32">mdi-plus</v-icon>
			</v-btn>
		</template>
		<template v-slot:toolbar-right>
			<v-text-field
				class="pt-0 mt-0"
				v-model="search"
				append-icon="mdi-magnify"
				label="Search"
				single-line
				hide-details
			></v-text-field>
		</template>
		<template v-slot:default>
			<v-data-table
				class="backup-table"
				:headers="headers"
				:items="akun"
				item-key="file_name"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.email="{ item }">
					<editable-cell 
						@edit="item.emailEdit = item.email"
						@finish="setEmail(item, item.emailEdit)"
						:change-detector="() => item.email != item.emailEdit"
						:confirm-text-maker="() => setEmailConfirmText(item)"
					>
						<template v-slot:editing>
							<v-text-field 
								name="email" 
								v-model="item.emailEdit" 
								:rules="emailRules"
								:counter="emailLenMax"
								type="email"
							/>
						</template>
						<template v-slot:default>
							<span>{{ item.email }}</span>
						</template>
					</editable-cell>
				</template>
				<template v-slot:item.role="{ item }">
					<editable-cell 
						@edit="item.roleEdit = item.role"
						@finish="setRole(item, item.roleEdit)"
						:change-detector="() => item.role != item.roleEdit"
						:confirm-text-maker="() => setRoleConfirmText(item)"
					>
						<template v-slot:editing>
							<v-select
								name="role"
								:items="roles"
								item-value="role"
								item-text="text"
								:value="rolesDict[item.role]"
								@change="value => item.roleEdit = value"
							></v-select>
						</template>
						<template v-slot:default>
							<span>{{ roleText(item.role) }}</span>
						</template>
					</editable-cell>
				</template>
				<template v-slot:item.enabled="{ item }">
					<v-tooltip bottom>
						<template v-slot:activator="{ on, attrs }">
						    <sync-checkbox 
						    	:input-value="item.enabled" 
						    	@change="value => setEnabled(item, value)"
						    	:confirm-text-maker="() => setEnabledConfirmText(item)"
						    	readonly
						    	v-bind="attrs" v-on="on"
					    	/>
						</template>
						<span>{{ item.enabled ? "Nonaktifkan" : "Aktifkan" }}</span>
					</v-tooltip>
				</template>
				<template v-slot:item.actions="{ item }">
					<v-tooltip bottom>
						<template v-slot:activator="{ on, attrs }">
							<v-btn 
								icon 
								@click.stop="prepareSetPassword(item)" 
								class=""
								v-bind="attrs"
								v-on="on"
							>
								<v-icon size="32" small>mdi-key-variant</v-icon>
							</v-btn>
						</template>
						<span>Ubah password</span>
					</v-tooltip>
				</template>
			</v-data-table>
			<simple-input-dialog 
				v-model="setPasswordDialog" 
				:on-confirm="setPassword"
				title="Ubah Password"
				:text="setPasswordText"
				label="Password Baru" 
				:password="true"
				:counter="passwordLenMax"
				:rules="passwordRules"
			/>
			<user-form-dialog
				v-model="createDialog"
				@register="user => { akun.push(user) }"
				:roles="roles"
			/>
		</template>
	</main-card>
</template>

<script>
import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/auth_types";
import { TUserError, TUserErrorCode, T_USER_ERROR_STR, EMAIL_LEN_MAX, PASSWORD_LEN_MAX } from "@/rpc/gen/user_types";
import { router } from "@/router/index";
import SimpleInputDialog from '@/components/general/SimpleInputDialog'
import { TAkunQuery } from '@/rpc/gen/akun_types';

import MainCard from '@/components/general/MainCard';
import SyncCheckbox from '@/components/general/SyncCheckbox';
import EditableCell from '@/components/general/EditableCell';
import UserFormDialog from '@/components/pengaturan/akun/UserFormDialog';
import { addEditFieldsBulk } from '@/lib/util';
import { EMAIL_RULES, PASSWORD_RULES } from '@/lib/validators/user';

@Component({
  	name: "AkunView",
  	components: {
  		SimpleInputDialog,
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		UserFormDialog
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.ADMIN_AKUN)
})
class AkunView extends BaseView {
	createDialog = false;
	setPasswordDialog = false;
	toSetPassword = null;
	roles = []
	rolesDict = {}
	search = ''
	headers = [
		{ text: 'Username', value: 'username' },
		{ text: 'Nama', value: 'name' },
		{ text: 'Email', value: 'email' },
		{ text: 'Role', value: 'role' },
		{ text: 'Aktif', value: 'enabled' },
		{ text: 'Aksi', value: 'actions' }
	]
	akun = []
	selfDisableWarning = " Akun ini adalah akun Anda sendiri. Anda akan logout dan tidak dapat login kembali hingga diaktifkan lagi."
	emailRules = EMAIL_RULES
	passwordRules = PASSWORD_RULES
	emailLenMax = EMAIL_LEN_MAX
	passwordLenMax = PASSWORD_LEN_MAX

	populateRoles(){
		for (const key in T_USER_ROLE_STR){
			if (key == TUserRole.SUPER_ADMIN && stores.auth.user.role != TUserRole.SUPER_ADMIN)
				continue;
			let obj = { role: key, text: T_USER_ROLE_STR[key] };
			this.roles.push(obj);
			this.rolesDict[key] = obj;
		}
	}

	roleText(role){
		return T_USER_ROLE_STR[role];
	}

	toggleUserEnabled(user){
		user.enabled = !user.enabled;
	}


	get disabledCount(){
		let count = 0;
		let i = 0;
		for(i = 0; i < this.akun.length; ++i){
			if (!this.akun[i].enabled) ++count;
		}
		return count;
	}

	async beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	async mounted(){
		stores.app.setBreadcrumbs([
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Pengaturan" },
			{ text: "Akun" },
		]);
		this.populateRoles();
		await this.fetchAkun();
	}
	async fetchAkun(){
		const view = this;
		view.busy = true;
		let query = new TAkunQuery();
		try{
			let akun = await stores.client.akun.fetch_akun(query);
			//this.akun = addEditFieldsBulk(akun, ["email", "role"]);
			this.akun = akun;
		} finally {
			view.busy = false;
		}
	}
	setEmailConfirmText(user){
		return "Apa Anda yakin ingin mengubah email untuk user '" 
			+ user.username + "' menjadi '" 
			+ user.emailEdit + "'?"
	}
	async setEmail(user, email){
		const view = this;
		view.busy=true;
		try{
			if (!email) throw new TUserError({ code: TUserErrorCode.EMAIL_EMPTY});
			await stores.client.akun.set_email(user.id, email);
			user.email = email;
			if (user.id == stores.auth.user.id) 
				await stores.auth.setUserEmail(user.email);
		} catch (error) {
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}

	setRoleConfirmText(user){
		return "Apa Anda yakin ingin mengubah role untuk user '" 
			+ user.username + "' menjadi '" 
			+ this.roleText(user.roleEdit) + "'?"
	}
	async setRole(user, role){
		const view = this;
		view.busy=true;
		try{
			if (!(role in  T_USER_ROLE_STR)) throw new TUserError({ code: TUserErrorCode.ROLE_INVALID});
			await stores.client.akun.set_role(user.id, role);
			user.role = role;
			if (user.id == stores.auth.user.id) 
				await stores.auth.setUserRole(user.role);
		} catch (error) {
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}
	setEnabledConfirmText(user){
		let action = user.enabled ? 'menonaktifkan' : 'mengaktifkan';
		let warn = (user.enabled && user.id == stores.auth.user.id) ? this.selfDisableWarning : "";
		return "Apa Anda yakin ingin " + action 
			+ " user '" + user.username + "'?" + warn;
	}
	async setEnabled(user, enabled){
		const view = this;
		view.busy=true;
		if (enabled === undefined || enabled === null)
			enabled = !user.enabled;
		try{
			await stores.client.akun.set_enabled(user.id, enabled);
			user.enabled = enabled;
			if (user.id == stores.auth.user.id){
				await stores.client.auth.logout();
			}
		} catch (error) {
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}
	prepareSetPassword(user){
		this.toSetPassword = user;
		this.setPasswordDialog = true;
	}
	get setPasswordText(){
		if (!this.toSetPassword) return '';
		return "Masukkan password baru untuk user '" 
			+ this.toSetPassword.username + "'"
	}
	async setPassword(password){
		const user = this.toSetPassword;
		const view = this;
		view.busy=true;
		try{
			await stores.client.akun.set_password(user.id, password);
			if (user.id == stores.auth.user.id){
				await stores.client.auth.login(stores.auth.user.username, password);
			}
		} catch (error) {
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}
	handleError(error){
		if (error instanceof TUserError){
			stores.app.pushTabDialog({
				title: "Error",
				text: T_USER_ERROR_STR[error.code]
			});
		}else{
			throw error;
		}
	}
}
export { AkunView } 
export default AkunView
</script>
<style scoped>
</style>
