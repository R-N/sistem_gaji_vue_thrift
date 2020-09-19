<template>
    <v-form ref="myForm" v-model="valid" @submit.prevent="reset" class="p-2" :disabled="busy">
		<card-title>
	        <h2 class="text-center">Reset Password</h2>
		</card-title>
		<v-card-text>
	    	<v-text-field 
	    		class="bigger-input" 
	    		label="Username/Email" 
	    		v-model="username" 
	    		:disabled="busy" 
	    		required
	    		:rules="[ v => !!v || 'Username/email harus diisi']"
    		/>
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy" :loading="busy">Reset</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>
import { TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR } from '@/rpc/gen/user.auth.errors_types';
import { TEmailError, TEmailErrorCode, T_EMAIL_ERROR_STR } from '@/rpc/gen/user.email.errors_types';

import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "ForgotPasswordForm",
	components: {
		CardTitle
	}
})
class ForgotPasswordForm extends WorkingComponent {
	valid = true;
	username = ''

	async reset(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.globalBusy = true;
		try{
			await stores.client.user.recovery.reset_password(this.username);
			stores.app.pushTabDialog({
				title: "Periksa Email Anda",
				text: "Link reset password telah dikirimkan ke alamat email akun Anda, jika username/email yang Anda masukkan benar."
			});
		} catch (error) {
			this.handleError(error);
		} finally {
			view.globalBusy = false;
		}
	}
	handleError(error){
		if (error instanceof TLoginError){
			stores.app.showError(T_LOGIN_ERROR_STR[error.code]);
		}else if (error instanceof TEmailError){
			stores.app.showError(T_EMAIL_ERROR_STR[error.code]);
		}else{
			throw error;
		}
	}
}
export { ForgotPasswordForm }
export default ForgotPasswordForm
</script>

<style scoped>
</style>
