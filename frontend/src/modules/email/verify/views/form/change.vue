<template>
    <v-form ref="myForm" v-model="valid" @submit.prevent="verify" class="p-2" :disabled="busy">
		<card-title>
	        <h2 class="text-center">Verifikasi Email</h2>
		</card-title>
		<v-card-text>
			<p>Untuk mengkonfirmasi email baru Anda, mohon login.</p>
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
	    		:rules="[ v => !!v || 'Password harus diisi']"
    		/>
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy" :loading="busy">Login</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>
import { TLoginError } from '@/rpc/gen/user.auth.errors_types';
import { TUserError } from "@/rpc/gen/user.user.errors_types";
import { TUserEmailError } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';

import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle';

@Component({
	name: "ChangeEmailForm",
	components: {
		CardTitle
	}
})
class ChangeEmailForm extends WorkingComponent {
	@Prop(String) token;
	valid = true;
	password = ''
	passwordVisible = false;

	async verify(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.busy = true;
		try{
			await stores.client.user.email.change_email(view.token, view.password);
			stores.app.pushTabDialog({
				title: "Berhasil",
				text: "Email Anda telah berhasil diubah.",
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
export { ChangeEmailForm }
export default ChangeEmailForm
</script>

<style scoped>
</style>
