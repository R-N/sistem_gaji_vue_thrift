
<script>

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { DialogBase } from '@/components/dialog/DialogBase';

@Component({
	name: "FormDialogBase",
	components: {
	}
})
class FormDialogBase extends DialogBase {

	close(){
		this.busy = false;
		this.myDialog = false;
		this.$emit('close');
	}
}
export { FormDialogBase }
export default FormDialogBase
</script>
