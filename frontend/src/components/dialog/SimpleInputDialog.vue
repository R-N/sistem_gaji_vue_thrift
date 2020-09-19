<template>
	<v-dialog
		v-model="myDialog"
		max-width="290"
		:persistent="busy"
	>
		<v-card>
			<v-form 
				ref="myForm"
				@submit.prevent.stop="confirm"
				v-model="valid"
			>
				<v-card-title class="headline">{{ title }}</v-card-title>
				<v-card-text>
					<p class="text-left">{{ text }}</p>
					<v-text-field 
						class="bigger-input" 
						v-if="!noInput && !password" 
						:label="label" 
						v-model="input" 
						:disabled="interactable" 
						required
						:rules="rules"
						:counter="counter"
					/>
					<v-text-field 
						class="bigger-input" 
						v-if="!noInput && password" 
						:label="label" 
						v-model="input" 
						:disabled="interactable" 
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
						:disabled="interactable" 
						type="password"
						required
						:counter="counter"
						:rules="confirmRules"
					/>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="green darken-1"
						text
						@click.stop="close()"
						:disabled="interactable"
					>
						Batal
					</v-btn>
					<v-btn
						type="submit"
						color="green darken-1"
						text
						:disabled="interactable"
						:loading="busy"
					>
						{{ confirmText }}
					</v-btn>
				</v-card-actions>
			</v-form>
		</v-card>
	</v-dialog>
</template>

<script>
import stores from '@/store/stores';

import { Component, Prop, Model, Watch } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
  	name: "SimpleInputDialog"
})
class SimpleInputDialog extends WorkingComponent {
	@Prop({ default: "Ok" }) confirmText;
	@Prop({ default: "Input Text" }) title;
	@Prop({ default: "" }) text;
	@Prop({ default: "" }) type;
	@Prop({ default: "Input" }) label;
	@Prop({ default: false }) password;
	@Prop({ default: false }) noInput;
	@Model('change', { type: Boolean }) dialog;
	@Prop(Function) onConfirm;
	@Prop({ default: undefined }) rules;
	@Prop({ default: undefined }) counter;
	valid = true;
	input = ''
	inputConfirm = ''
	passwordVisible = false;

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

	@Watch('myDialog', { immediate: false })
	onDialogChange(val, oldVal){
		if( this.$refs.myForm){
			this.$refs.myForm.resetValidation();
		}
		this.input = ''
		this.inputConfirm = ''
	}


	validateConfirm(inputConfirm){
		if (this.input === inputConfirm) return true;
		return "Konfirmasi tidak sama";
	}

	get confirmRules(){
		return [
			v => !!v || "Konfirmasi tidak boleh kosong",
			this.validateConfirm
		];
	}

	get interactable(){
		return this.busy || !this.dialog;
	}

	close(){
		this.busy = false;
		this.myDialog = false;
	}

	async confirm(){
		this.$refs.myForm.validate();
		if(!this.valid){
			return;
		}
		if(!this.noInput && this.password && this.input != this.inputConfirm){
			stores.app.pushTabDialog({
				title: "Error",
				text: "Konfirmasi salah"
			});
			return;
		}
		this.busy = true;
		if(this.onConfirm){
			if(this.noInput){
				await this.onConfirm();
			}else{
				await this.onConfirm(this.input);
			}
		}else{
			if(this.noInput){
				this.$emit("confirm");
			}else{
				this.$emit("confirm", this.input);
			}
		}
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
