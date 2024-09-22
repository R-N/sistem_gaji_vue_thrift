<template>
	<confirmation-slot
		class="d-flex text-center justify-center justify-self-center"
		:confirmTextMaker="confirmTextMaker"
		:on-confirm="change"
		:parent-busy="busy"
	>
		<template v-slot="{ ask }">
			<v-tooltip bottom :disabled="disabled || !text">
				<template v-slot:activator="{ on, attrs }">
					<v-checkbox 
						:name="name"
						:input-value="inputValue"
						:value="value"
						@click.prevent.capture="() => tryAsk(ask)"
						readonly
						class="text-center justify-center justify-self-center"
						:disabled="disabled"
					/>
				</template>
				<span>aa{{ text }}</span>
			</v-tooltip>
		</template>
	</confirmation-slot>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
  	name: "SyncCheckbox",
  	components: {
  		ConfirmationSlot
  	}
})
class SyncCheckbox extends WorkingComponent {
	@Prop(String) name;
	@Prop(String) value;
	@Prop({ default: false }) inputValue;
	@Prop([String, Function]) confirmTextMaker; 
	@Prop({ default: false }) disabled;
	@Prop(String) textEnable;
	@Prop(String) textDisable;
	@Prop(Function) onChange;
	@Prop({default: true}) ask;

	async tryAsk(ask){
		if (!this.disabled){
			if (this.ask)
				await ask();
			else
				await this.change();
		}
	}

	get text(){
		return this.inputValue ? this.textDisable :this. textEnable;
	}
	async change(){
        if (this.onChange){
            this.busy = true;
            await this.onChange(!this.inputValue);
            this.busy = false;
        } else{
            this.$emit('change', !this.inputValue);
        }
	}
}
export { SyncCheckbox } 
export default SyncCheckbox
</script>
<style scoped>
</style>
