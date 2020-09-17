<template>
    <v-form ref="myForm" v-model="valid" @submit.prevent="send" class="p-2" :disabled="busy">
		<card-title>
	        <h2 class="text-center">Verifikasi Email</h2>
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
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy || isLoggedIn" :loading="busy">Kirim</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/general/WorkingComponent';
import stores from "@/store/stores";
import { TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR } from '@/rpc/gen/auth_types';
import { router } from '@/router/index';
import CardTitle from '@/components/general/CardTitle'

@Component({
	name: "ResendVerificationForm",
	components: {
		CardTitle
	}
})
class ResendVerificationForm extends WorkingComponent {
	valid = true;
	username = ''

	async send(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.globalBusy = true;
		try{
			await stores.client.auth.resend_verification(this.username);
			stores.app.pushTabDialog({
				title: "Periksa Email Anda",
				text: "Link verifikasi email telah dikirimkan ke email akun Anda, jika username/email yang Anda masukkan benar."
			});
		} catch (error) {
			if (error instanceof TLoginError){
				stores.app.pushTabDialog({
					title: "Error",
					text: T_LOGIN_ERROR_STR[error.code]
				});
			}else{
				throw error;
			}
		} finally {
			view.globalBusy = false;
		}
	}
}
export { ResendVerificationForm }
export default ResendVerificationForm
</script>

<style scoped>
</style>
