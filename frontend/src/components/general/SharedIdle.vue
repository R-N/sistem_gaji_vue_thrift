<template>
	<div></div>
</template>
<script>
import { Vue, Component, Prop, PropSync, Watch } from 'vue-property-decorator';
import { appStore } from '@/store/stores';

@Component({
	name: "SharedIdle",
	model: {
		prop: 'idle',
		event: 'update:idle',
	}
})
class SharedIdle extends Vue {
	@Prop(Number) idleWait;
	@PropSync('idle', { type: Boolean }) syncedIdle
	idleTimer = null;

	get idleWaitMillis(){
		return this.idleWait * 1000;
	}

	get sharedUserPresent(){
		return appStore.userPresent;
	}

	@Watch('sharedUserPresent')
	onSharedUserPresent(val, oldVal) {
		if (val != oldVal && val && this.syncedIdle) {
			console.log("Present");
			this.syncedIdle = false;
		}
	}

	mounted(){
		const comp = this;
		this.idleTimer = window.setInterval(function(){
			if (appStore.getIdleTime() >= comp.idleWaitMillis && !comp.syncedIdle){
				comp.syncedIdle = true;
			}
		}, 1000);
	}

	beforeDestroy(){
		if(this.idleTimer){
			window.clearInterval(this.idleTimer);
			this.idleTimer = null;
		}
	}
}
export { SharedIdle }
export default SharedIdle
</script>
<style scoped>
</style>