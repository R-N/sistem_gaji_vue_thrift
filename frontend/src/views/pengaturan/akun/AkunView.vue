<template>
	<main-card title="Akun">
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
				:items="akun"
				item-key="id"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.email="{ item }">
					<editable-cell 
						v-if="mayEditEmail(item) || isSuperAdmin"
						@edit="item.emailEdit = item.email"
						@finish="setEmail(item, item.emailEdit)"
						:change-detector="() => item.email != item.emailEdit"
						:confirm-text-maker="() => setEmailConfirmText(item)"
						:parent-busy="busy"
					>
						<template v-slot:editing>
							<v-text-field 
								name="email" 
								v-model="item.emailEdit" 
								:rules="emailRules"
								:counter="emailLenMax"
								type="email"
								:disabled="busy"
							/>
						</template>
						<template v-slot:default>
							<span>{{ item.email }}</span>
						</template>
					</editable-cell>
					<span v-else >{{ item.email }}</span>
				</template>
				<template v-slot:item.role="{ item }">
					<editable-cell 
						v-if="mayEdit(item)"
						@edit="item.roleEdit = item.role"
						@finish="setRole(item, item.roleEdit)"
						:change-detector="() => item.role != item.roleEdit"
						:confirm-text-maker="() => setRoleConfirmText(item)"
						:parent-busy="busy"
					>
						<template v-slot:editing>
							<v-select
								name="role"
								:items="roles"
								item-value="role"
								item-text="text"
								:value="rolesDict[item.role]"
								@change="value => item.roleEdit = value"
								:disabled="busy"
							></v-select>
						</template>
						<template v-slot:default>
							<span>{{ roleText(item.role) }}</span>
						</template>
					</editable-cell>
					<span v-else >{{ item.email }}</span>
				</template>
				<template v-slot:item.enabled="{ item }">
					<v-tooltip 
						v-if="mayEdit(item)"
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
				<template v-slot:item.verified="{ item }">
					<v-tooltip 
						v-if="isSuperAdmin"
						bottom
					>
						<template v-slot:activator="{ on, attrs }">
						    <sync-checkbox 
						    	:input-value="item.verified" 
						    	@change="value => setVerified(item, value)"
						    	:confirm-text-maker="() => setVerifiedConfirmText(item)"
						    	readonly
						    	v-bind="attrs" v-on="on"
								:disabled="busy"
					    	/>
						</template>
						<span>{{ item.enabled ? "Batalkan verifikasi" : "Paksa verifikasi" }}</span>
					</v-tooltip>
					<span v-else>
					    <v-simple-checkbox 
					    	:value="item.verified" 
					    	disabled
				    	/>
				    </span>
				</template>
				<template v-slot:item.actions="{ item }">
					<v-tooltip 
						bottom
					>
						<template v-slot:activator="{ on, attrs }">
							<v-btn 
								icon 
								@click.stop="prepareSetPassword(item)" 
								class=""
								v-bind="attrs"
								v-on="on"
								:disabled="busy"
							>
								<v-icon size="32" small>mdi-key-variant</v-icon>
							</v-btn>
						</template>
						<span>Ubah password</span>
					</v-tooltip>
					<confirmation-slot
						class="text-center justify-center justify-self-center"
						:confirmTextMaker="deleteText(item)"
						v-slot="{ ask }"
						:on-confirm="() => deleteUser(item)"
						v-if="isSuperAdmin"
					>
						<v-tooltip bottom>
							<template v-slot:activator="{ on, attrs }">
								<v-btn 
									icon 
									@click.stop="askDeleteUser(item, ask)" 
									class="" 
									v-bind="attrs" 
									v-on="on"
									:disabled="busy"
								>
									<v-icon size="32" small>mdi-delete</v-icon>
								</v-btn>
							</template>
							<span>Hapus</span>
						</v-tooltip>
					</confirmation-slot>
				</template>
			</v-data-table>
			<simple-input-dialog 
				v-if="isSuperAdmin"
				v-model="setPasswordDialog" 
				:on-confirm="setPassword"
				title="Ubah Password"
				:text="setPasswordText"
				label="Password Baru" 
				:password="true"
				:counter="passwordLenMax"
				:rules="passwordRules"
				:disabled="busy"
			/>
			<user-form-dialog
				v-model="createDialog"
				@register="user => { akun.push(user) }"
				:roles="roles"
				:parent-busy="busy"
			/>
		</template>
	</main-card>
</template>

<script>
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';
import { TUserRole, T_USER_ROLE_STR, T_USER_ROLE_DOUBLES } from "@/rpc/gen/user.user.types_types";
import { 
	TUserError, 
	EMAIL_LEN_MAX, PASSWORD_LEN_MAX 
} from "@/rpc/gen/user.user.errors_types";
import { TUserQuery } from '@/rpc/gen/user.management.structs_types';

import { router } from "@/router/index";
import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { EMAIL_RULES, PASSWORD_RULES } from '@/lib/validators/user';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import SimpleInputDialog from '@/components/dialog/SimpleInputDialog'
import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/form/SyncCheckbox';
import EditableCell from '@/components/form/EditableCell';

import UserFormDialog from '@/views/pengaturan/akun/UserFormDialog';
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot'

@Component({
  	name: "AkunView",
  	components: {
  		SimpleInputDialog,
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		UserFormDialog,
		ConfirmationSlot,
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
	akun = []
	selfDisableWarning = " Akun ini adalah akun Anda sendiri, sehingga anda akan logout dan tidak dapat login kembali hingga diaktifkan lagi."
	selfDeleteWarning = " Akun ini adalah akun Anda sendiri, sehingga anda akan logout dan tidak dapat menggunakan akun ini lagi secara permanen."
	roleLogoutWarning = " Akun yang diubah role nya harus login ulang."
	selfRoleLogoutWarning = " Akun ini adalah akun Anda sendiri, sehingga Anda akan logout otomatis."
	selfRoleDownWarning = " Selain itu, jika Anda bukan Admin Akun maupun Super Admin, Anda tidak bisa mengakses halaman ini."
	emailRules = EMAIL_RULES
	passwordRules = PASSWORD_RULES
	emailLenMax = EMAIL_LEN_MAX
	passwordLenMax = PASSWORD_LEN_MAX


	get headers(){
		let headers = [
			{ text: 'Username', value: 'username' },
			{ text: 'Nama', value: 'name' },
			{ text: 'Email', value: 'email' },
			{ text: 'Role', value: 'role' },
			{ text: 'Aktif', value: 'enabled', align: 'center' },
			{ text: 'Terverifikasi', value: 'verified', align: 'center' }
		]
		if (this.isSuperAdmin){
			headers.push({ text: 'Aksi', value: 'actions' })
		}
		return headers
	}

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

	get isSuperAdmin(){
		return stores.auth.user.role == TUserRole.SUPER_ADMIN;
	}

	mayEdit(user){
		return user.role != TUserRole.SUPER_ADMIN || this.isSuperAdmin;
	}

	mayEditEmail(user){
		return this.mayEdit(user) && !user.verified;
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
		let query = new TUserQuery();
		try{
			let akun = await stores.client.user.management.fetch_akun(query);
			//this.akun = addEditFieldsBulk(akun, ["email", "role"]);
			this.akun = akun;
		} catch(error){
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	setEmailConfirmText(user){
		return "Apa Anda yakin ingin mengubah email untuk user '" 
			+ user.email + "' menjadi '" 
			+ user.emailEdit + "'?"
	}
	async setEmail(user, email){
		const view = this;
		view.busy=true;
		try{
			await stores.client.user.management.set_email(user.id, email);
			user.email = email;
			user.verified = false;
			if (user.id == stores.auth.user.id) 
				await stores.auth.setUserEmail(user.email);
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setRoleConfirmText(user){
		let warn = this.roleLogoutWarning;
		if (user.id == stores.auth.user.id){
			warn += this.selfRoleLogoutWarning;
			if (!T_USER_ROLE_DOUBLES[TUserRole.ADMIN_AKUN].includes(parseInt(user.roleEdit))){
				warn += this.selfRoleDownWarning;
			}
		}
		return "Apa Anda yakin ingin mengubah role untuk user '" 
			+ this.roleText(user.role) + "' menjadi '" 
			+ this.roleText(user.roleEdit) + "'?" + warn;
	}
	async setRole(user, role){
		const view = this;
		view.busy=true;
		try{
			if (!(role in  T_USER_ROLE_STR)) throw new TUserError({ code: TUserErrorCode.ROLE_INVALID});
			await stores.client.user.management.set_role(user.id, role);
			user.role = role;
			/*
			if (user.id == stores.auth.user.id){
				stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
			}
			*/
		} catch (error) {
			view.showError(error);
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
			await stores.client.user.management.set_enabled(user.id, enabled);
			user.enabled = enabled;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setVerifiedConfirmText(user){
		let action = user.verified ? 'membatalkan verifikasi' : 'memaksa verifikasi';
		let warn = (user.verified && user.id == stores.auth.user.id) ? this.selfDisableWarning : "";
		return "Apa Anda yakin ingin " + action 
			+ " user '" + user.username + "'?" + warn;
	}
	async setVerified(user, verified){
		const view = this;
		view.busy=true;
		if (verified === undefined || verified === null)
			verified = !user.verified;
		try{
			await stores.client.user.management.set_verified(user.id, verified);
			user.verified = verified;
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	deleteText(user){
		let warn = (user.enabled && user.id == stores.auth.user.id) ? this.selfDeleteWarning : "";
		return "Apa Anda yakin ingin menghapus user '" + user.username + "'?" + warn;
	}

	async askDeleteUser(user, ask){
		if (user.verified){
			this.showError("Tidak dapat menghapus akun yang telah terverifikasi.");
			return;
		}
		ask();
	}

	async deleteUser(user){
		const view = this;
		view.busy=true;
		try{
			await stores.client.user.management.delete(user.id);
			this.akun.pop(user);
		} catch (error) {
			view.showError(error);
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
			await stores.client.user.management.set_password(user.id, password);
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}
	showError(error){
		if (stores.helper.error.showFilteredError(error, 
			[TUserError, TEmailError, TUserEmailError]
		)) return;
		throw error;
	}
}
export { AkunView } 
export default AkunView
</script>
<style scoped>
</style>
