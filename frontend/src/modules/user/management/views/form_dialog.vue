<template>
	<form-dialog
		max-width="400"
		:parent-busy="busy"
		:on-submit="register"
		title="Buat Akun"
		:disabled="disabled"
		:on-reset="reset"
		v-model="myDialog"
	>
        <template v-slot:fields="{ interactable, busy }">
			<v-text-field 
				name="username"
				class="bigger-input" 
				label="Username" 
				v-model="username" 
				:disabled="!interactable" 
				required
				:rules="usernameRules"
				:counter="usernameMaxLen"
			/>
			<v-text-field 
				name="name"
				class="bigger-input" 
				label="Nama" 
				v-model="name" 
				:disabled="!interactable" 
				required
				:rules="nameRules"
				:counter="nameMaxLen"
			/>
			<v-text-field 
				name="email"
				class="bigger-input" 
				label="Email" 
				v-model="email" 
				:disabled="!interactable" 
				required
				:rules="emailRules"
				type="email"
				:counter="emailMaxLen"
			/>
			<v-select
				class="bigger-input" 
				name="role"
				:items="roles"
				item-value="role"
				item-text="text"
				v-model="role"
				@change="setRole"
				:return-object="true"
			></v-select>
			<v-text-field 
				v-if="false"
				name="password"
				class="bigger-input" 
				label="Password" 
				v-model="password" 
				:disabled="!interactable" 
				required
				:append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
				@click:append="() => { passwordVisible = !passwordVisible }"
				:type="passwordVisible ? 'text' : 'password'"
				:rules="passwordRules"
				:counter="passwordMaxLen"
			/>
			<v-text-field 
				v-if="false"
				class="bigger-input" 
				label="Konfirmasi Password"
				v-model="passwordConfirm" 
				:disabled="!interactable" 
				type="password"
				required
				:counter="passwordMaxLen"
				:rules="confirmRules"
			/>
        </template>
	</form-dialog>
</template>

<script>
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';
import { 
	TUserError, 
	USERNAME_MAX_LEN, NAME_MAX_LEN, EMAIL_MAX_LEN, PASSWORD_MAX_LEN 
} from "@/rpc/gen/user.user.errors_types";
import { TUserRegistrationForm } from "@/rpc/gen/user.management.structs_types";

import stores from "@/store/stores";
import { USERNAME_RULES, PASSWORD_RULES, NAME_RULES, EMAIL_RULES, ROLE_RULES } from '@/lib/validators/user';

import { Component, Prop, Watch } from 'vue-property-decorator';

import { FormDialog } from '@/components/form/FormDialog'
import { FormDialogBase } from '@/components/form/FormDialogBase'

@Component({
	name: "UserFormDialog",
	components: {
		FormDialog,
	}
})
class UserFormDialog extends FormDialogBase {
	@Prop({ default: false }) disabled;
	@Prop({ default: [] }) roles;
	username = ''
	name = ''
	email = ''
	password = ''
	passwordConfirm = ''
	role = null
	passwordVisible = false;

	usernameRules = USERNAME_RULES
	nameRules = NAME_RULES
	emailRules = EMAIL_RULES
	passwordRules = PASSWORD_RULES
	roleRules = ROLE_RULES

	usernameMaxLen = USERNAME_MAX_LEN
	nameMaxLen = NAME_MAX_LEN
	emailMaxLen = EMAIL_MAX_LEN
	passwordMaxLen = PASSWORD_MAX_LEN

	reset(){
		this.username = ''
		this.name = ''
		this.email = ''
		this.password =''
		this.passwordConfirm = ''
		if(this.roles) 
			this.role = this.roles[0]
		else
			this.role = null;
	}

	@Watch('roles')
	onRolesSet(val, oldVal){
		if(val) 
			this.role = val[0];
		else
			this.role = null;
	}

	validateConfirm(passwordConfirm){
		if (this.password === passwordConfirm) return true;
		return "Konfirmasi password tidak sama";
	}

	get confirmRules(){
		return [
			v => !!v || "Konfirmasi tidak boleh kosong",
			this.validateConfirm
		];
	}

	setRole(value){
		this.role = value;
	}

	async register(form){
		const view = this;
		view.busy = true;
		form = new TUserRegistrationForm({
			username: this.username,
			name: this.name,
			//password: this.password,
			email: this.email,
			role: this.role.role
		});
		try{
			let user = await stores.client.user.management.create(form);
			view.$emit("register", user);
			view.close();
		} catch (error) {
			if (stores.helper.error.showFilteredError(error, 
				[TUserError, TEmailError, TUserEmailError]
			)) return;
			throw error;
		} finally {
			view.busy = false;
		}
	}
}
export { UserFormDialog }
export default UserFormDialog
</script>

<style scoped>
</style>
