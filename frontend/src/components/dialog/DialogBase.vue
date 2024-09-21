
<script>

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';
import { BaseView } from '@/views/BaseView';

@Component({
	name: "DialogBase",
	components: {
	}
})
class DialogBase extends BaseView {
	@Model('change', { type: [Boolean, String, Object, Array] }) dialog;

	@Watch('myDialog', { immediate: false })
	onDialogChange(val, oldVal){
		if(this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
		if (this.reset)
	        this.reset();
	}
	close(){
		this.busy = false;
		this.myDialog = false;
		this.$emit('close');
	}
	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			if (this.reset)
	            this.reset();
			this.busy = false;
		}
		this.$emit('change', value);
	}
}
export { DialogBase }
export default DialogBase
</script>
