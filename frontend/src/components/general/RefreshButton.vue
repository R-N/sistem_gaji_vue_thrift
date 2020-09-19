<template>
	<v-btn :icon="icon" :large="large" @click.stop="refresh">
		<slot><v-icon>fa-redo</v-icon></slot>
	</v-btn>
</template>

<script>
import { appStore } from '@/store/modules/app';

import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
	name: "RefreshButton"
})
class RefreshButton extends Vue {
	@Prop({ default: true }) icon;
	@Prop({ default: true }) large;
	async refresh(){
		appStore.setRouterBusy(true);
		if(!appStore.globalBusy && !appStore.authBusy){
			window.location.reload();
		}else{
			appStore.setAuthBusy(false);
			appStore.setGlobalBusy(false);
			appStore.setGlobalRefresh(true);
		}
	}
}
export { RefreshButton }
export default RefreshButton
</script>
<style scoped>
</style>