<template>
	<span class="d-flex text-center justify-center justify-self-center">
	    <v-checkbox 
	    	:name="name"
	    	:input-value="inputValue"
	    	:value="value"
	    	@click.prevent.capture="onClick()"
	    	readonly
	    	class="text-center justify-center justify-self-center"
	    	:disabled="disabled"
		/>
		<simple-input-dialog 
			v-if="confirmTextMaker"
			v-model="confirmDialog" 
			:on-confirm="emitChange"
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
  	name: "SyncCheckbox",
  	components: {
  		SimpleInputDialog
  	}
})
class SyncCheckbox extends Vue {
	@Prop(String) name;
	@Prop(String) value;
	@Prop({ default: false }) inputValue;
	@Prop(Function) confirmTextMaker; 
	@Prop({ default: false }) disabled;
	confirmText = '';
	confirmDialog = false;

	emitChange(){
		this.$emit('change', !this.inputValue)
	}
	onClick(){
		if(!this.confirmTextMaker){
			this.emitChange();
		}else{
			this.confirmText = this.confirmTextMaker();
			this.confirmDialog = true;
		}
	}
}
export { SyncCheckbox } 
export default SyncCheckbox
</script>
<style scoped>
</style>
