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
					<refresh-button icon large v-if="mayRefresh"/>
				</v-progress-circular>
			</v-row>
		</v-container>
	</v-overlay>
</template>

<script>
import { appStore } from '@/store/modules/app';

import { Component, Prop, Watch } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import RefreshButton from '@/components/general/RefreshButton';

@Component({
	name: "LoadingOverlay",
	components: {
		RefreshButton
	}
})
class LoadingOverlay extends WorkingComponent {
	@Prop({ default: 96 }) circleSizeRefresh
	@Prop({ default: 64 }) circleSizeNormal
	@Prop({ default: 5 }) mayRefreshWait

	mayRefresh = false;
	mayRefreshTimer = null;

	mounted(){
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

}
export { LoadingOverlay }
export default LoadingOverlay
</script>
<style scoped>
</style>