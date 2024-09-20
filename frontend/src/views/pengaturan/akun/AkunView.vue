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
				:items="items"
				item-key="id"
				:search="search"
				:loading="busy"
			>
				<template v-slot:item.email="{ item }">
					<editable-cell-text-field
						v-if="mayEditEmail(item)"
						name="email" 
						type="email"
						:counter="emailLenMax"
						:confirm-text-maker="(value) => setFieldConfirmText('email', item, value)"
						:value="item.email" 
						@change="(value) => setEmail(item, value)"
						:rules="emailRules"
						:disabled="!mayEditEmail(item) || busy"
					/>
					<span v-else >{{ item.email }}</span>
				</template>
				<template v-slot:item.role="{ item }">
					<editable-cell-select
						v-if="mayEdit(item)"
						name="role" 
						item-value="role"
						item-title="text"
						:value="rolesDict[item.role]"
						:items="roles"
						:confirm-text-maker="(value) => setRoleConfirmText(item, value)"
						@change="(value) => setRole(item, value)"
						:disabled="!mayEdit(item) || busy"
					/>
					<span v-else >{{ item.role }}</span>
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
					<confirmation-icon-button
						icon="mdi-delete"
						text="Hapus"
						:confirmTextMaker="deleteConfirmText(item)"
						:on-confirm="() => deleteItem(item)"
						:ask="(ask) => askDelete(item, ask)" 
						:disabled="busy"
						v-if="isSuperAdmin"
					/>
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
				@register="user => { items.push(user) }"
				:roles="roles"
				:parent-busy="busy"
			/>
		</template>
	</main-card>
</template>

<script>
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';
import { TUserManagementError, TUserManagementErrorCode } from '@/rpc/gen/user.management.errors_types';
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
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';
import BaseCrudView from '@/views/BaseCrudView';

import ConfirmationIconButton from '@/components/form/buttons/ConfirmationIconButton';
import EditableCellTextField from '@/components/form/editable_cells/EditableCellTextField';
import EditableCellSelect from '@/components/form/editable_cells/EditableCellSelect';

@Component({
  	name: "AkunView",
  	components: {
  		SimpleInputDialog,
  		MainCard,
  		SyncCheckbox,
  		EditableCell,
  		UserFormDialog,
		ConfirmationSlot,
		ConfirmationIconButton,
		EditableCellTextField,
		EditableCellSelect,
  	},
	beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.ADMIN_AKUN)
})
class AkunView extends BaseCrudView {
	setPasswordDialog = false;
	toSetPassword = null;
	roles = []
	rolesDict = {}
	rolesText = {}
	selfDisableWarning = " Akun ini adalah akun Anda sendiri, sehingga anda akan logout dan tidak dapat login kembali hingga diaktifkan lagi."
	selfDeleteWarning = " Akun ini adalah akun Anda sendiri, sehingga anda akan logout dan tidak dapat menggunakan akun ini lagi secara permanen."
	roleLogoutWarning = " Akun yang diubah role nya harus login ulang."
	selfRoleLogoutWarning = " Akun ini adalah akun Anda sendiri, sehingga Anda akan logout otomatis."
	selfRoleDownWarning = " Selain itu, jika Anda bukan Admin Akun maupun Super Admin, Anda tidak bisa mengakses halaman ini."
	emailRules = EMAIL_RULES
	passwordRules = PASSWORD_RULES
	emailLenMax = EMAIL_LEN_MAX
	passwordLenMax = PASSWORD_LEN_MAX

	get nameField(){ return "username"; }
    get itemNameLower(){ return 'akun'; }
    get client(){ return stores.client.user.management; }
    get query(){ return new TUserQuery(); }
	get breadcrumbs(){
		return [
			{ text: "Beranda", to: { name: 'beranda' }, exact: true },
			{ text: "Pengaturan" },
			{ text: "Akun" },
		]
	}
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
	get filteredErrors() { return [TUserError, TEmailError, TUserEmailError, TUserManagementError]; }

	populateRoles(){
		for (const key in T_USER_ROLE_STR){
			if (key == TUserRole.SUPER_ADMIN && !this.isSuperAdmin)
				continue;
			let obj = { role: key, text: T_USER_ROLE_STR[key] };
			this.roles.push(obj);
			this.rolesDict[key] = obj;
			this.rolesText[key] = obj.text;
		}
	}

	roleText(role){
		return T_USER_ROLE_STR[role];
	}

	mayEdit(user){
		return T_USER_ROLE_DOUBLES[user.role].includes(stores.auth.user.role);
	}

	mayEditEmail(user){
		return this.mayEdit(user) && !user.verified;
	}

	async mounted(){
		await this._mounted();
		this.populateRoles();
	}
	setEmailConfirmText(user, newValue){
		return this.setFieldConfirmText("email", user, newValue);
	}

	async setEmail(user, email){
		const view = this;
		view.busy=true;
		try{
			await this.setField("email", user, email, false);
			user.verified = false;
			if (user.id == stores.auth.user.id) 
				await stores.auth.setUserEmail(user.email);
		} catch (error) {
			view.showError(error);
		} finally {
			view.busy = false;
		}
	}

	setRoleConfirmText(user, newValue){
		let warn = this.roleLogoutWarning;
		if (user.id == stores.auth.user.id){
			warn += this.selfRoleLogoutWarning;
			if (!T_USER_ROLE_DOUBLES[TUserRole.ADMIN_AKUN].includes(parseInt(user.roleEdit))){
				warn += this.selfRoleDownWarning;
			}
		}
		return this.setFieldConfirmText("role", user, newValue, this.rolesText) + warn;
	}

	async setRole(user, role){
		const view = this;
		view.busy=true;
		try{
			if (!(role in  T_USER_ROLE_STR)) throw new TUserError({ code: TUserErrorCode.ROLE_INVALID});
			await this.setField("role", user, role, false);
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
	setEnabledConfirmText(user, newValue){
		let warn = (user.enabled && user.id == stores.auth.user.id) ? this.selfDisableWarning : "";
        return this._setEnabledConfirmText(user, newValue) + warn;
	}
	setVerifiedConfirmText(user){
		let warn = (user.verified && user.id == stores.auth.user.id) ? this.selfDisableWarning : "";
		return this.toggleFieldConfirmText("verified", 'membatalkan verifikasi', 'memaksa verifikasi', user, "username") + warn;
	}
	async setVerified(user, verified){
		return await this.toggleField("verified", user, verified);
	}

	deleteConfirmText(user){
		let warn = (user.enabled && user.id == stores.auth.user.id) ? this.selfDeleteWarning : "";
        return this._deleteConfirmText(user) + warn;
	}

	async askDelete(user, ask){
		if (user.verified){
			this.showError(new TUserManagementError({ code: TUserManagementErrorCode.CANNOT_DELETE_VERIFIED}));
			return;
		}
        return this._askDelete(user, ask);
	}

	prepareSetPassword(user){
		this.toSetPassword = user;
		this.setPasswordDialog = true;
	}
	get setPasswordText(){
		if (!this.toSetPassword) return '';
		return `Masukkan password baru untuk user '${this.toSetPassword.username}'`
	}
	async setPassword(password){
		return await this.setField("password", this.toSetPassword, password);
	}
}
export { AkunView } 
export default AkunView
</script>
<style scoped>
</style>
