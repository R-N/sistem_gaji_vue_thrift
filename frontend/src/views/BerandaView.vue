<template>
	<v-main v-if="isLoggedIn">
		<v-container
			class="fill-height"
			fluid
		>
			<v-row
				align="center"
				justify="center"
				class="flex-column"
			>
		    	<v-btn raised color="primary" class="text-center mx-0" @click="hello" :loading="busy">Hello Admin Utama</v-btn>
		        <h4 class="text-center mb-4" v-if="msg">{{ msg }}</h4>
			</v-row>
		</v-container>
	</v-main>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import { authStore, clientStore, appStore } from "@/store/stores";
import { TAuthError, TAuthErrorCode } from "@/rpc/gen/auth_types";
import { router } from "@/router/index";

@Component({
  	name: "BerandaView",
	//beforeRouteEnter: authRouter.routeRequireLoginNow
})
class BerandaView extends BaseView {
	msg = ''

	beforeMount(){
		//if(!routeRequireLoginNow()) return;
	}
	
	async hello(){
		const view = this;
		view.busy=true;
		try{
			this.msg = await clientStore.hello.hello_admin_utama();
		} catch (error){
			if (error instanceof TAuthError && error.code === TAuthErrorCode.INVALID_ROLE){
				this.msg = "You're not admin utama!";
			}else{
				console.log(error);
			}
		} finally {
			view.busy = false;
		}
	}
}
export { BerandaView } 
export default BerandaView
</script>

<style scoped>

</style>
