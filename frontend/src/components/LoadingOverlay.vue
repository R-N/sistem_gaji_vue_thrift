<template>
	<v-overlay :value="busy">
		<v-container
			class="fill-height"
			fluid
		>
			<v-row
				align="center"
				justify="center"
				class="flex-column"
				>
				<v-progress-circular indeterminate :size="circleSize">
					<v-btn icon large @click.stop="refresh" v-if="mayRefresh">
						<v-icon>fa-redo</v-icon>
					</v-btn>
				</v-progress-circular>
			</v-row>
		</v-container>
	</v-overlay>
</template>

<script>
import { Component, Prop, Watch } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';
import { appStore } from '@/store/modules/app';

@Component({
	name: "LoadingOverlay"
})
class LoadingOverlay extends WorkingComponent {
	@Prop({ default: 96 }) circleSizeRefresh
	@Prop({ default: 64 }) circleSizeNormal
	@Prop({ default: 5 }) mayRefreshWait

	mayRefresh = false;
	mayRefreshTimer = null;

	mounted(){
		console.log("mayRefreshWait: " + this.mayRefreshWait);
		this.setTimer(this.busy);
	}

	get mayRefreshWaitMillis(){
		return this.mayRefreshWait * 1000;
	}
	get circleSize(){
		return this.mayRefresh ? this.circleSizeRefresh : this.circleSizeNormal;
	}

	@Watch('busy')
	onBusyChanged(val, oldVal){
		console.log("Busy changed: " + val);
		if (val != oldVal){
			this.setTimer(val);
		}
	}

	setTimer(busy){
		if (this.mayRefreshTimer) window.clearTimeout(this.mayRefreshTimer);
		if (busy){
			const comp = this;
			this.mayRefreshTimer = window.setTimeout(function(){
				comp.mayRefresh = true;
			}, this.mayRefreshWaitMillis);
		} else {
			this.mayRefreshTimer = null;
			this.mayRefresh = false;
		}
	}

	async refresh(){
		appStore.setRouterBusy(true);
		if(!this.globalBusy){
			window.location.reload();
		}else{
			appStore.setGlobalBusy(false);
			appStore.setGlobalRefresh(true);
		}
	}
}
export { LoadingOverlay }
export default LoadingOverlay
</script>
<style scoped>
</style>