<template>
	
	<v-tooltip bottom :disabled="disabled || !text">
		<template v-slot:activator="{ on, attrs }">
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
		<span>{{ text }}</span>
	</v-tooltip>
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
	@Prop(String) textEnable;
	@Prop(String) textDisable;

	get text(){
		return this.inputValue ? this.textDisable :this. textEnable;
	}
	emitChange(){
		this.$emit('change', !this.inputValue)
	}
}
export { SyncCheckbox } 
export default SyncCheckbox
</script>
<style scoped>
</style>
