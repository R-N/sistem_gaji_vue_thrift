<template>
	<v-card class="p-4">
	    <form id="form-login" @submit.prevent="login" class="p-2">
	        <h2 class="text-center">Sistem Gaji</h2>
	        <h2 class="text-center mb-4">PT. X</h2>
	    	<v-text-field class="login-input" label="Username" v-model="username" :disabled="busy" required/>
	    	<v-text-field class="login-input" label="Password" type="password" v-model="password" :disabled="busy" required/>
	    	<v-btn raised color="primary" type="submit" class="text-center w-100 mx-0" :disabled="busy || isLoggedIn" :loading="busy">Login</v-btn>
	    </form>
	</v-card>
</template>

<script>

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';
import { authStore, clientStore, appStore } from "@/store/stores";
import { router } from '@/router/index';

@Component({
	name: "LoginForm"
})
class LoginForm extends WorkingComponent {
	username = ''
	password = ''
	msg = ''

	get isLoggedIn(){
		return authStore.isLoggedIn;
	}

	get name(){
		if (!authStore.user) return '';
		return authStore.user.name;
	}

	async login(){
		const view = this;
		view.globalBusy = true;
		try{
			await clientStore.auth.login(this.username, this.password);
			await router.safePush({ name: "beranda" });
		} catch (error){
			console.log(error);
		} finally {
			view.globalBusy = false;
		}
	}

}
export { LoginForm }
export default LoginForm
</script>

<style scoped>
.login-input >>> input, .login-input >>> label{
	font-size: 1.2em;
}
</style>
