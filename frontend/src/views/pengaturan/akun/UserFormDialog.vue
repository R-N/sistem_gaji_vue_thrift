<template>
	<v-dialog
		v-model="myDialog"
		max-width="400"
		:persistent="busy"
	>
		<v-card class="">
		    <v-form ref="myForm" v-model="valid" @submit.prevent="register" class="p-2" :disabled="!interactable">
				<v-card-title class="headline">Buat Akun</v-card-title>
				<v-card-text>
			    	<v-text-field 
			    		name="username"
			    		class="bigger-input" 
			    		label="Username" 
			    		v-model="username" 
			    		:disabled="!interactable" 
			    		required
			    		:rules="usernameRules"
						:counter="usernameLenMax"
		    		/>
			    	<v-text-field 
			    		name="name"
			    		class="bigger-input" 
			    		label="Nama" 
			    		v-model="name" 
			    		:disabled="!interactable" 
			    		required
			    		:rules="nameRules"
						:counter="nameLenMax"
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
						:counter="emailLenMax"
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
			    		:counter="passwordLenMax"
		    		/>
					<v-text-field 
			    		v-if="false"
						class="bigger-input" 
						label="Konfirmasi Password"
						v-model="passwordConfirm" 
						:disabled="!interactable" 
						type="password"
						required
						:counter="passwordLenMax"
						:rules="confirmRules"
					/>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn
							color="green darken-1"
							text
							@click.stop="close()"
							:disabled="!interactable"
						>
							Batal
						</v-btn>
						<v-btn
							type="submit"
							color="green darken-1"
							text
							:disabled="!interactable"
							:loading="busy"
						>
							Ok
						</v-btn>
					</v-card-actions>
				</v-card-text>
		    </v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';
import { TUserRole, T_USER_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { 
	TUserError, 
	USERNAME_LEN_MAX, NAME_LEN_MAX, EMAIL_LEN_MAX, PASSWORD_LEN_MAX 
} from "@/rpc/gen/user.user.errors_types";
import { TUserRegistrationForm } from "@/rpc/gen/user.management.structs_types";

import stores from "@/store/stores";
import { USERNAME_RULES, PASSWORD_RULES, NAME_RULES, EMAIL_RULES, ROLE_RULES } from '@/lib/validators/user';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "UserFormDialog",
	components: {
		CardTitle
	}
})
class UserFormDialog extends WorkingComponent {
	@Prop({ default: false }) disabled;
	@Model('change', { type: Boolean }) dialog;
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

	usernameLenMax = USERNAME_LEN_MAX
	nameLenMax = NAME_LEN_MAX
	emailLenMax = EMAIL_LEN_MAX
	passwordLenMax = PASSWORD_LEN_MAX


	valid = true;

	@Watch('myDialog')
	onDialogChange(val, oldVal){
		if( this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
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

	close(){
		this.busy = false;
		this.myDialog = false;
	}

	get interactable(){
		return !this.disabled && !this.busy;
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

	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.input = '';
			this.busy = false;
		}
		this.$emit('change', value);
	}

	setRole(value){
		this.role = value;
	}

	async register(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		let form = new TUserRegistrationForm({
			username: this.username,
			name: this.name,
			//password: this.password,
			email: this.email,
			role: this.role.role
		});
		try{
			let user = await stores.client.user.management.register_akun(form);
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
