<template>
    <confirmation-slot
        class="text-center justify-center justify-self-center"
        :confirmTextMaker="confirmTextMaker"
        v-slot="{ ask }"
        :on-confirm="() => onConfirm()"
    >
        <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn 
                    icon 
                    @click.stop="tryAsk(ask)" 
                    class="" 
                    v-bind="attrs" 
                    v-on="on"
                    :disabled="busy || disabled"
                >
                    <v-icon size="32" small>{{ icon }}</v-icon>
                </v-btn>
            </template>
            <span>{{ text }}</span>
        </v-tooltip>
    </confirmation-slot>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';
import WorkingComponent from '@/components/WorkingComponent';

@Component({
  	name: "ConfirmationIconButton",
  	components: {
        ConfirmationSlot
  	}
})
class ConfirmationIconButton extends WorkingComponent {
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
