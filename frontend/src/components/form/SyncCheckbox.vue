<template>
	<confirmation-slot
		class="d-flex text-center justify-center justify-self-center"
		:confirmTextMaker="confirmTextMaker"
		v-slot="{ ask }"
		:on-confirm="emitChange"
	>
	    <v-checkbox 
	    	:name="name"
	    	:input-value="inputValue"
	    	:value="value"
	    	@click.prevent.capture="if(!disabled) ask()"
	    	readonly
	    	class="text-center justify-center justify-self-center"
	    	:disabled="disabled"
		/>
	</confirmation-slot>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';

@Component({
  	name: "SyncCheckbox",
  	components: {
  		ConfirmationSlot
  	}
})
class SyncCheckbox extends Vue {
	@Prop(String) name;
	@Prop(String) value;
	@Prop({ default: false }) inputValue;
	@Prop([String, Function]) confirmTextMaker; 
	@Prop({ default: false }) disabled;

	emitChange(){
		this.$emit('change', !this.inputValue)
	}
}
export { SyncCheckbox } 
export default SyncCheckbox
</script>
<style scoped>
</style>
