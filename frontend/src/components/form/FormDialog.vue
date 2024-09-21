<template>
	<v-dialog
		v-model="myDialog"
		:max-width="maxWidth"
		:persistent="busy"
	>
		<v-card class="">
		    <v-form ref="myForm" v-model="valid" class="p-2" :disabled="!interactable" @submit.prevent="submit" >
				<v-card-title class="headline">{{ title }}</v-card-title>
				<v-card-text>
		            <slot name="fields" :interactable="interactable" :busy="busy" :disabled="disabled"></slot>
					<v-card-actions>
		                <slot name="buttons-left" :interactable="interactable" :busy="busy" :disabled="disabled"></slot>
						<v-spacer></v-spacer>
		                <slot name="buttons" :interactable="interactable" :busy="busy" :disabled="disabled"></slot>
		                <slot name="buttons-right" :interactable="interactable" :busy="busy" :disabled="disabled"></slot>
						<v-btn
							color="green darken-1"
							text
							@click.stop="close()"
							:disabled="!interactable"
                            v-if="cancelText"
						>
							Batal
						</v-btn>
						<v-btn
							type="submit"
							color="green darken-1"
							text
							:disabled="!interactable"
							:loading="busy"
                            v-if="confirmText"
						>
							Ok
						</v-btn>
					</v-card-actions>
				</v-card-text>
		    </v-form>
		</v-card>
	</v-dialog>
</template>

<script>

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
	name: "FormDialog",
	components: {
	}
})
class FormDialog extends WorkingComponent {
	@Prop({ default: false }) disabled;
	@Model('change', { type: Boolean }) dialog;
	@Prop({ default: "Batal" }) cancelText;
	@Prop({ default: "Ok" }) confirmText;
	@Prop({ default: 400 }) maxWidth;
	@Prop({ default: "Form" }) title;
    @Prop(Function) reset;

	valid = true;

	@Watch('myDialog')
	onDialogChange(val, oldVal){
		if( this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
        if (this.reset)
            this.reset();
	}

	close(){
		this.busy = false;
		this.myDialog = false;
		this.$emit('close');
	}

	get interactable(){
		return !this.disabled && !this.busy;
	}

	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.busy = false;
		}
		this.$emit('change', value);
	}
	async submit(){
		this.$refs.myForm.validate();
		if(!this.valid) return;
		this.$emit('submit', this.$refs.myForm);
	}
}
@Component({
	name: "FormDialogBase",
	components: {
	}
})
class FormDialogBase extends WorkingComponent {
	@Model('change', { type: Boolean }) dialog;

	close(){
		this.busy = false;
		this.myDialog = false;
		this.$emit('close');
	}
	get myDialog(){
		return this.dialog;
	}
	set myDialog(value){
		if(value == this.dialog) return;
		if (!value){
			this.busy = false;
		}
		this.$emit('change', value);
	}
}
export { FormDialog, FormDialogBase }
export default FormDialog
</script>

<style scoped>
</style>
