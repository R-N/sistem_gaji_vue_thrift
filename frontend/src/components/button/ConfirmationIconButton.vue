<template>
    <confirmation-slot
        class="text-center justify-center justify-self-center"
        :confirmTextMaker="confirmTextMaker"
        
        :on-confirm="() => onConfirm()"
    >
		<template v-slot="{ ask }">
            <icon-button
                @click.stop="tryAsk(ask)" 
                :disabled="busy || disabled"
                :icon="icon"
                :text="text"
                :size="size"
                :small="small"
            />
        </template>
    </confirmation-slot>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';
import WorkingComponent from '@/components/WorkingComponent';
import IconButton from '@/components/button/IconButton';

@Component({
  	name: "ConfirmationIconButton",
  	components: {
        ConfirmationSlot,
        IconButton
  	}
})
class ConfirmationIconButton extends WorkingComponent {
    @Prop({default: 32}) size;
    @Prop({default: true}) small;
    @Prop(String) icon;
    @Prop(String) text;
	@Prop([String, Function]) confirmTextMaker; 
	@Prop(Function) ask; 
	@Prop(Function) onConfirm; 
	@Prop({ default: false }) disabled;
	@Prop({ default: null }) item;

    tryAsk(ask){
        if (this.ask){
            this.ask(ask);
        }else{
            ask();
        }
    }
}
export { ConfirmationIconButton } 
export default ConfirmationIconButton
</script>
<style scoped>
</style>
