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
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy" :loading="busy">Kirim</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>
import { TUserError } from '@/rpc/gen/user.user.errors_types';
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';

import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

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
			await stores.client.user.recovery.resend_verification(this.username);
			stores.app.pushTabDialog({
				title: "Periksa Email Anda",
				text: "Link verifikasi email telah dikirimkan ke email akun Anda, jika username/email yang Anda masukkan benar."
			});
		} catch (error) {
			if (stores.helper.error.showFilteredError(error, 
				[TUserError, TEmailError, TUserEmailError]
			)) return;
			throw error;
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
