<script>
import { authStore } from "@/store/stores";

import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
	name: "BaseView"
})
class BaseView extends WorkingComponent {

}

export { BaseView }
export default BaseView
</script>