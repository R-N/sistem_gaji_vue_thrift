
<script>

import { Vue, Component, Prop } from 'vue-property-decorator'
import { appStore } from '@/store/stores';


@Component({
	name: "WorkingComponent"
})
class WorkingComponent extends Vue {
	@Prop({ default: false }) parentBusy
	selfBusy = false

	get busy(){
		return this.selfBusy || this.parentBusy || appStore.routerBusy || appStore.tabBusy || appStore.globalBusy
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
