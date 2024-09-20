
<script>
import { appStore } from '@/store/stores';

import { Vue, Component, Prop } from 'vue-property-decorator'


@Component({
	name: "WorkingComponent"
})
class WorkingComponent extends Vue {
	@Prop({ default: false }) parentBusy
	selfBusy = false

	log(x){
		console.log(x);
	}

	get busy(){
		return this.selfBusy || this.parentBusy || appStore.routerBusy || appStore.tabBusy || appStore.authBusy || appStore.globalBusy
	}

	set busy(busy){
		this.selfBusy = busy;
	}

	get globalBusy(){
		return appStore.globalBusy;
	}

	set globalBusy(busy){
		appStore.setGlobalBusy(busy);
	}

	get authBusy(){
		return appStore.authBusy;
	}

	set authBusy(busy){
		appStore.setAuthBusy(busy);
	}

	get tabBusy(){
		return appStore.tabBusy;
	}

	set tabBusy(busy){
		appStore.setTabBusy(busy);
	}
}
export { WorkingComponent }
export default WorkingComponent
</script>
