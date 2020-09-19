<script>
import { authStore } from "@/store/stores";

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
	name: "BaseView"
})
class BaseView extends WorkingComponent {
	get isLoggedIn(){
		return authStore.isLoggedIn;
	}
	get userRole(){
		return authStore.role;
	}
}

export { BaseView }
export default BaseView
</script>