<template>
	<span>
	    <v-checkbox 
	    	:name="name"
	    	:input-value="inputValue"
	    	:value="value"
	    	@click.prevent.capture="onClick()"
	    	readonly
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
import SimpleInputDialog from '@/components/SimpleInputDialog';

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
