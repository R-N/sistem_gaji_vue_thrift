<template>
    <v-form v-model="valid" ref="myForm" @submit.prevent="login" class="p-2" :disabled="busy">
		<card-title>
	        <h2 class="text-center">Sistem Gaji</h2>
	        <h2 class="text-center ">PT. X</h2>
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
	    	<v-text-field 
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
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy || isLoggedIn" :loading="busy">Login</v-btn>
		</v-card-text>
    </v-form>
</template>

<script>
import { TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR } from '@/rpc/gen/user.auth.errors_types';

import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
	name: "LoginForm",
	components: {
		CardTitle
	}
})
class LoginForm extends WorkingComponent {
	valid = true;
	username = ''
	password = ''
	passwordVisible = false;

	get isLoggedIn(){
		return stores.auth.isLoggedIn;
	}

	async login(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		const view = this;
		view.globalBusy = true;
		try{
			await stores.client.user.auth.login(this.username, this.password);
			await router.safePush({ name: "beranda" });
		} catch (error) {
			this.handleError(error);
		} finally {
			view.globalBusy = false;
		}
	}
	handleError(error){
		if (error instanceof TLoginError){
			stores.app.showError(T_LOGIN_ERROR_STR[error.code]);
		}else{
			throw error;
		}
	}

}
export { LoginForm }
export default LoginForm
</script>

<style scoped>
</style>
