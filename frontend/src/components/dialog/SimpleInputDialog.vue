<template>
	<form-dialog
		max-width="290"
		:parent-busy="busy"
		:title="title"
		:disabled="disabled"
		v-model="myDialog"
		:on-reset="reset"
		:on-cancel="onCancel"
		:on-submit="submit"
	>
        <template v-slot:fields="{ interactable, busy }">
			<p class="text-left">{{ text }}</p>
			<v-text-field 
				class="bigger-input" 
				v-if="!noInput && !password" 
				:label="label" 
				v-model="input" 
				:disabled="!interactable" 
				required
				:rules="rules"
				:counter="counter"
			/>
			<v-text-field 
				class="bigger-input" 
				v-if="!noInput && password" 
				:label="label" 
				v-model="input" 
				:disabled="!interactable" 
				:append-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
				@click:append="() => { passwordVisible = !passwordVisible }"
				:type="passwordVisible ? 'text' : 'password'"
				required
				:rules="rules"
				:counter="counter"
			/>
			<v-text-field 
				class="bigger-input" 
				v-if="!noInput && password" 
				:label="'Konfirmasi ' + label" 
				v-model="inputConfirm" 
				:disabled="!interactable" 
				type="password"
				required
				:counter="counter"
				:rules="confirmRules"
			/>
		</template>
	</form-dialog>
</template>

<script>
import stores from '@/store/stores';

import { Component, Prop, Model, Watch } from 'vue-property-decorator';
import { FormDialogBase } from '@/components/form/FormDialogBase';
import { FormDialog } from '@/components/form/FormDialog';

@Component({
  	name: "SimpleInputDialog",
	components:{
		FormDialog
	}
})
class SimpleInputDialog extends FormDialogBase {
	@Prop(Function) onCancel;
	@Prop(Function) onSubmit;

	@Prop({ default: false }) disabled;
	@Prop({ default: "Batal" }) cancelText;
	@Prop({ default: "Ok" }) confirmText;
	@Prop({ default: 400 }) maxWidth;
	@Prop({ default: "Input Text" }) title;

	@Prop({ default: "" }) text;
	@Prop({ default: "" }) type;
	@Prop({ default: "Input" }) label;
	@Prop({ default: false }) password;
	@Prop({ default: false }) noInput;
	@Prop([Array, Function]) rules;
	@Prop([Function, Number]) counter;
	input = ''
	inputConfirm = ''
	passwordVisible = false;

	reset(){
		this.input = '';
		this.inputConfirm = ''
	}

	validateConfirm(inputConfirm){
		return this.input === inputConfirm;
	}

	getValue(){
		return this.input;
	}

	get confirmRules(){
		return [
			v => !!v || "Konfirmasi tidak boleh kosong",
			v => this.validateConfirm(v) || "Konfirmasi tidak sama"
		];
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
