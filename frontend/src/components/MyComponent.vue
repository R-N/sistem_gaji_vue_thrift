
<script>
import { appStore, authStore, settingsStore } from '@/store/stores';

import { Vue, Component, Prop } from 'vue-property-decorator'


@Component({
	name: "MyComponent"
})
class MyComponent extends Vue {

	log(x){
		console.log(x);
	}
	get isSuperAdmin(){
		return authStore.isSuperAdmin;
	}
	get isLoggedIn(){
		return authStore.isLoggedIn;
	}
	get userRole(){
		return authStore.role;
	}
	get perusahaanId(){
		return settingsStore.perusahaanId;
	}
	get perusahaanName(){
		return settingsStore.perusahaanName;
	}
	get serverReachable(){
		return appStore.serverReachable;
	}
}
export { MyComponent }
export default MyComponent
</script>
