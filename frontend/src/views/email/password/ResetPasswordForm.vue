<template>
    <v-form ref="myForm" v-model="valid" @submit.prevent="reset" class="p-2" :disabled="busy">
		<card-title>
	        <h2 class="text-center">Reset Password</h2>
		</card-title>
		<v-card-text>
			<p>Masukkan password baru:</p>
	    	<v-text-field 
	    		name="password"
	    		class="bigger-input" 
	    		label="Password" 
	    		v-model="password" 
	    		:disabled="busy" 
	    		required
			    :append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
			    @click:append="() => { passwordVisible = !passwordVisible }"
			    :type="passwordVisible ? 'text' : 'password'"
	    		:rules="passwordRules"
	    		:counter="passwordLenMax"
    		/>
			<v-text-field 
				class="bigger-input" 
				label="Konfirmasi Password"
				v-model="passwordConfirm" 
				:disabled="busy" 
				type="password"
				required
				:counter="passwordLenMax"
				:rules="confirmRules"
			/>
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy" :loading="busy">Simpan</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>
import { TLoginError } from '@/rpc/gen/user.auth.errors_types';
import { TUserError, PASSWORD_MAX_LEN } from "@/rpc/gen/user.user.errors_types";
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';

import stores from "@/store/stores";
import { router } from '@/router/index';
import { PASSWORD_RULES } from '@/lib/validators/user';

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle';

@Component({
	name: "ResetPasswordForm",
	components: {
		CardTitle
	}
})
class ResetPasswordForm extends WorkingComponent {
	@Prop(String) token;
	valid = true;
	password = ''
	passwordConfirm = ''
	passwordVisible = false;
	passwordRules = PASSWORD_RULES
	passwordLenMax = PASSWORD_MAX_LEN
	
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

	async reset(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		try{
			await stores.client.user.email.set_password(view.token, view.password);
			stores.app.pushTabDialog({
				title: "Berhasil",
				text: "Reset Password Berhasil. Silahkan login.",
				onDismiss: function(){ router.safePush({ name: "beranda" }) }
			});
		} catch (error) {
			if (stores.helper.error.showFilteredError(error, 
				[TLoginError, TUserError, TEmailError, TUserEmailError]
			)) return;
			throw error;
		} finally {
			view.busy = false;
		}
	}
}
export { ResetPasswordForm }
export default ResetPasswordForm
</script>

<style scoped>
</style>
