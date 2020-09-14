<template>
	<v-card class="">
		<card-title>
	        <h2 class="text-center">Sistem Gaji</h2>
	        <h2 class="text-center ">PT. X</h2>
		</card-title>
		<v-card-text>
		    <v-form @submit.prevent="login" class="p-2" :disabled="busy">
		    	<v-text-field 
		    		class="bigger-input" 
		    		label="Username" 
		    		v-model="username" 
		    		:disabled="busy" 
		    		required
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
	    		/>
		    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy || isLoggedIn" :loading="busy">Login</v-btn>
		    </v-form>
		</v-card-text>
	</v-card>
</template>

<script>

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';
import stores from "@/store/stores";
import { TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR } from '@/rpc/gen/auth_types';
import { router } from '@/router/index';
import CardTitle from '@/components/CardTitle'

@Component({
	name: "LoginForm",
	components: {
		CardTitle
	}
})
class LoginForm extends WorkingComponent {
	username = ''
	password = ''
	passwordVisible = false;

	get isLoggedIn(){
		return stores.auth.isLoggedIn;
	}

	async login(){
		const view = this;
		view.globalBusy = true;
		try{
			await stores.client.auth.login(this.username, this.password);
			await router.safePush({ name: "beranda" });
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
export { LoginForm }
export default LoginForm
</script>

<style scoped>
</style>
