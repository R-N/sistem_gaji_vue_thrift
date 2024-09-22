<template>
	<span>
		<slot :ask="ask"></slot>
		<simple-input-dialog 
			v-if="confirmTextMaker && confirmDialog"
			v-model="confirmDialog" 
			:on-submit="emitConfirm"
			:on-cancel="onCancel"
			title="Konfirmasi"
			:text="confirmText"
			no-input="true"
		/>
	</span>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

import SimpleInputDialog from '@/components/dialog/SimpleInputDialog';

@Component({
  	name: "ConfirmationSlot",
  	components: {
  		SimpleInputDialog
  	}
})
class ConfirmationSlot extends Vue {
	@Prop([String, Function]) confirmTextMaker; 
	@Prop(Function) onConfirm;
	@Prop(Function) onCancel; 
	confirmText = '';
	confirmDialog = false;

	emitConfirm(){
		if(this.onConfirm){
			this.onConfirm();
		}else{
			this.$emit('confirm');
		}
	}
	ask(){
		if(!this.confirmTextMaker){
			this.emitConfirm();
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
