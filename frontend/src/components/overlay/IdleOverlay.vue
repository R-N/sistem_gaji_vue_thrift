<template>
	<div>
	    <v-overlay :value="logoutTimer">
	    	<v-row align="center" justify="center" class="flex-column">
		    	<h3>Anda akan otomatis logout dalam</h3>
		    	<h2>{{ logoutCountdownMinutes }}:{{ logoutCountdownSeconds }}</h2>
		    </v-row>
	    </v-overlay>
	    <shared-idle :idle-wait="idleWait" v-model="idle"/>
	</div>
</template>
<script>
import { appStore, authStore, clientStore } from '@/store/stores';
import { authRouter } from '@/router/routers/auth';

import { Vue, Component, Prop, Watch } from 'vue-property-decorator';

import SharedIdle from '@/components/general/SharedIdle';


@Component({
	name: "IdleOverlay",
	components: {
		SharedIdle
	}
})
class IdleOverlay extends Vue {
	@Prop(Number) logoutWait;
	@Prop(Number) idleWait;

	logoutCountdown = 0;
	logoutTimer = null;


	mounted(){
	}

	get logoutCountdownMinutes(){
		return ('0' + parseInt(this.logoutCountdown/60)).slice(-2);
	}
	get logoutCountdownSeconds(){
		return ('0' + parseInt(this.logoutCountdown%60)).slice(-2);
	}
	get idle(){
		return appStore.idle;
	}
	set idle(value){
		if (!value) this.stopCountdown();
		else appStore.setIdle();
	}

	get isLoggedIn(){
		return authStore.isLoggedIn;
	}

	async logout(){
		this.stopCountdown();
		await clientStore.user.auth.logout();
		const comp = this;
		authRouter.dialogIdleLogout();
	}

	stopCountdown(){
		if (this.logoutTimer){
			window.clearInterval(this.logoutTimer);
			this.logoutTimer = null;
			this.logoutCountdown = -1;
		}
	}

	startCountdown(){
		this.stopCountdown();
		this.logoutCountdown = this.logoutWait;
		const comp = this;
		this.logoutTimer = window.setInterval(function(){
			comp.logoutCountdown--;
		}, 1000);
	}
	@Watch('idle')
	onIdle(val, oldVal){
		if (val != oldVal){
			if (val && this.isLoggedIn){
				this.startCountdown();
			}else{
				this.stopCountdown();
			}
		}
	}
	@Watch('logoutCountdown')
	onLogoutCountdownTick(val, oldVal){
		if (oldVal > val && val == 0){
			if(this.isLoggedIn) this.logout();
			else this.stopCountdown();
		}
	}
	@Watch('isLoggedIn')
	onAuthChanged(val, oldVal){
		if (val != oldVal && !val){
			this.stopCountdown();
		}
	}
	beforeDestroy(){
		this.stopCountdown();
	}
}
export { IdleOverlay }
export default IdleOverlay
</script>
<style scoped>
</style>