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
import { BaseView } from '@/views/BaseView';
import { DialogBase } from '@/components/dialog/DialogBase';
import { FormDialogBase } from '@/components/form/FormDialogBase';

@Component({
	name: "FormDialog",
	components: {
	}
})
class FormDialog extends FormDialogBase {
	@Prop(Function) onCancel;
	@Prop(Function) onSubmit;
    @Prop(Function) onReset;
    @Prop(Function) onValidate;
	@Prop({ default: false }) disabled;
	@Prop({ default: "Batal" }) cancelText;
	@Prop({ default: "Ok" }) confirmText;
	@Prop({ default: 400 }) maxWidth;
	@Prop({ default: "Form" }) title;
}
export { FormDialog }
export default FormDialog
</script>

<style scoped>
</style>
