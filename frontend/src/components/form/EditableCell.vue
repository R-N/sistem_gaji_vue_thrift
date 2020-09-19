<template>
	<div class="d-flex flex-grow-1">
		<v-form 
			class="flex-grow-1" 
			ref="myForm" 
			@submit.native.prevent.stop="finishEdit"
			v-model="valid"
			:disabled="busy"
		>
			<div class="d-flex align-center justify-space-between">
				<span class="flex-grow-1">
					<slot v-if="readOnlyMode || editing" name="editing" :readonly="readOnlyMode && !editing" :editing="editing">Edit</slot>
					<slot v-else name="default">Hello</slot>
				</span>
				<span  class="flex-grow-0 flex-shrink-0">
					<span v-if="editing">
						<v-tooltip bottom key="submit">
							<template v-slot:activator="{ on, attrs }">
								<v-btn 
									icon 
									type="submit"  
									v-bind="attrs" 
									v-on="on"
									:disabled="busy"
								>
									<v-icon size="32" small>mdi-check</v-icon>
								</v-btn>
							</template>
							<span>Simpan</span>
						</v-tooltip>
						<v-tooltip bottom key="cancel">
							<template v-slot:activator="{ on, attrs }">
								<v-btn 
									icon 
									@click.stop="cancelEdit();" 
									v-bind="attrs" 
									v-on="on"
									:disabled="busy"
								>
									<v-icon size="32" small>mdi-cancel</v-icon>
								</v-btn>
							</template>
							<span>Batal</span>
						</v-tooltip>
					</span>
					<span v-else>
						<v-tooltip bottom key="edit">
							<template v-slot:activator="{ on, attrs }">
								<v-btn 
									icon 
									@click.stop="beginEdit();" 
									v-bind="attrs" 
									v-on="on"
									:disabled="busy"
								>
									<v-icon size="32" small>mdi-pencil</v-icon>
								</v-btn>
							</template>
							<span>Ubah</span>
						</v-tooltip>
					</span>
				</span>
			</div>
		</v-form>
		<simple-input-dialog 
			v-if="confirmTextMaker"
			v-model="confirmDialog" 
			:on-confirm="onConfirmFinish"
			title="Konfirmasi"
			:text="confirmText"
			no-input="true"
		/>
	</div>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import WorkingComponent from '@/components/WorkingComponent';

import SimpleInputDialog from '@/components/dialog/SimpleInputDialog'

@Component({
  	name: "SyncCheckbox",
  	components: {
  		SimpleInputDialog
  	}
})
class SyncCheckbox extends WorkingComponent {
	@Prop(Function) onFinish;
	@Prop(Function) onEdit;
	@Prop(Function) onCancel;
	@Prop(Function) confirmTextMaker; 
	@Prop(Function) changeDetector;
	@Prop({ default: false }) readOnlyMode;
	editing=false;
	confirmText = '';
	confirmDialog = false;
	valid=true;

	async beginEdit(){
		if(this.onEdit)
			await this.onEdit();
		else
			this.$emit("edit");
		this.editing = true;
	}
	async cancelEdit(){
		this.editing = false;
		if(this.onCancel)
			await this.onCancel();
		else
			this.$emit("cancel");
		this.$refs.myForm.resetValidation();
	}
	async finishEdit(){
		if(!this.valid) return;
		if(this.changeDetector && !this.changeDetector()){
			await this.cancelEdit();
			return;
		}
		if(!this.confirmTextMaker){
			await this.onConfirmFinish();
			return;
		}else{
			this.confirmText = this.confirmTextMaker();
			this.confirmDialog = true;
		}
	}
	async onConfirmFinish(){
		//this.$emit("submit", e);
		let form = this.$refs.myForm.$el;
		let formData = Object.fromEntries(new FormData(form).entries());
		if(this.onFinish)
			await this.onFinish(formData);
		else
			this.$emit("finish", formData);
		this.editing = false;
	}
}
export { SyncCheckbox } 
export default SyncCheckbox
</script>
<style scoped>
</style>
