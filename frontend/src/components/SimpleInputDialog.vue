<template>
	<v-dialog
		v-model="myDialog"
		max-width="290"
	>
		<v-card>
			<v-form @submit.prevent.stop="confirm">
				<v-card-title class="headline">{{ title }}</v-card-title>
				<v-card-text>
					<p class="text-left">{{ text }}</p>
					<v-text-field class="bigger-input" v-if="!noInput" :label="label" v-model="input" :disabled="busy"/>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="green darken-1"
						text
						@click.stop="close()"
					>
						Batal
					</v-btn>
					<v-btn
						type="submit"
						color="green darken-1"
						text
					>
						{{ confirmText }}
					</v-btn>
				</v-card-actions>
			</v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import { Component, Prop, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
  	name: "SimpleInputDialog"
})
class SimpleInputDialog extends WorkingComponent {
	@Prop({ default: "Ok" }) confirmText;
	@Prop({ default: "Input Text" }) title;
	@Prop({ default: "" }) text;
	@Prop({ default: "Input" }) label;
	@Prop({ default: false }) noInput;
	@Model('change', { type: Boolean }) dialog;
	@Prop(Function) onConfirm;
	input = ''

	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.input = '';
			this.busy = false;
		}
		this.$emit('change', value);
	}

	close(){
		this.myDialog = false;
	}

	async confirm(){
		this.busy = true;
		if(this.onConfirm) await this.onConfirm(this.input);
		this.close();
	}
}
export { SimpleInputDialog } 
export default SimpleInputDialog
</script>
<style scoped>
.backup-table{
	background: #00000000;
}
</style>
