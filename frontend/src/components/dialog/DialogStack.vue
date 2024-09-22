<template>
	<v-dialog v-model="item" persistent max-width="290" v-if="item">
		<v-card>
			<v-card-title class="headline" v-if="item.title">{{ item.title }}</v-card-title>
			<v-card-text v-if="item.text">{{ item.text }}</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn ref="closeButton" color="green darken-1" text @click="item = null" :disabled="!item">{{ closeText }}</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
	name: "DialogStack"
})
class DialogStack extends Vue {
	@Prop(Array) items
	@Prop({default: "Tutup"}) closeText;

	get item(){
		if (this.items.length == 0) return null;
		return this.items[this.items.length-1];
	}
	set item(value){
		if (!value){
			if (this.item.onDismiss) this.item.onDismiss();
			this.$emit('dialogstackpop');
		}
	}

}
export { DialogStack }
export default DialogStack
</script>
<style scoped>
</style>