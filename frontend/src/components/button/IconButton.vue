<template>
    <v-tooltip bottom :disabled="disabled || !text">
        <template v-slot:activator="{ on, attrs }">
            <v-btn 
                icon 
                class="" 
                v-bind="attrs" 
                v-on="on"
                :disabled="disabled"
				@click="$emit('click', $event)" 
            >
                <v-icon size="32" small>{{ icon }}</v-icon>
            </v-btn>
        </template>
        <span>{{ text }}</span>
    </v-tooltip>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import ConfirmationSlot from '@/components/dialog/ConfirmationSlot';

@Component({
  	name: "IconButton",
  	components: {
        ConfirmationSlot
  	}
})
class IconButton extends Vue {
    @Prop(String) icon;
    @Prop(String) text;
    @Prop({default: false}) disabled;
}
export { IconButton } 
export default IconButton
</script>
<style scoped>
</style>
