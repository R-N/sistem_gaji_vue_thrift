<template>
	<span>
		<slot :ask="ask"></slot>
		<simple-input-dialog 
			v-if="confirmTextMaker && confirmDialog"
			v-model="confirmDialog" 
			:on-submit="confirm"
			:on-cancel="onCancel"
			title="Konfirmasi"
			:text="confirmText"
			no-input="true"
			:parent-busy="busy"
		/>
	</span>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

import SimpleInputDialog from '@/components/dialog/SimpleInputDialog';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
  	name: "ConfirmationSlot",
  	components: {
  		SimpleInputDialog
  	}
})
class ConfirmationSlot extends WorkingComponent {
	@Prop([String, Function]) confirmTextMaker; 
	@Prop(Function) onConfirm;
	@Prop(Function) onCancel; 
	confirmText = '';
	confirmDialog = false;

	confirm(){
		if(this.onConfirm){
			this.busy = true;
			this.onConfirm();
		}else{
			this.$emit('confirm');
		}
		this.confirmDialog = false;
		this.busy = false;
	}
	ask(){
		if(!this.confirmTextMaker){
			this.confirm();
		}else{
			if (this.confirmTextMaker instanceof Function){
				this.confirmText = this.confirmTextMaker();
			}else if (typeof this.confirmTextMaker === 'string' || this.confirmTextMaker instanceof String){
				this.confirmText = this.confirmTextMaker;
			}else{
				this.confirmText = '';
			}
			this.confirmDialog = true;
		}
	}
}
export { ConfirmationSlot } 
export default ConfirmationSlot
</script>
<style scoped>
</style>
