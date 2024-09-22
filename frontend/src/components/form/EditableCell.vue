<template>
	<confirmation-slot
		:confirmTextMaker="confirmTextMaker"
		v-slot="{ ask }"
		:on-confirm="onConfirmFinish"
		class="d-flex flex-grow-1"
	>
		<v-form 
			class="flex-grow-1" 
			ref="myForm" 
			@submit.native.prevent.stop="finishEdit(ask)"
			v-model="valid"
			:disabled="busy"
		>
			<div class="d-flex align-left justify-space-between" v-if="title">
				<span class="font-weight-bold">{{ title }}</span>
			</div>
			<div class="d-flex align-center justify-space-between">
				<span class="flex-grow-1">
					<slot v-if="editing && !(disabled || busy)" name="editing" :readonly="disabled || busy || !editing" :disabled="disabled || busy || !editing" :editing="editing"></slot>
					<slot v-else name="default"></slot>
				</span>
				<span class="flex-grow-0 flex-shrink-0" v-if="!(disabled || busy)">
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
	</confirmation-slot>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import WorkingComponent from '@/components/WorkingComponent';

import ConfirmationSlot from '@/components/dialog/ConfirmationSlot'

@Component({
  	name: "EditableCell",
  	components: {
  		ConfirmationSlot
  	}
})
class EditableCell extends WorkingComponent {
	@Prop(String) title;
	@Prop(Function) onFinish;
	@Prop(Function) onEdit;
	@Prop(Function) onCancel;
	@Prop([String, Function]) confirmTextMaker; 
	@Prop(Function) changeDetector;
	@Prop({ default: false }) disabled;
	confirmDialog=false;
	editing=false;
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
	async finishEdit(ask=null){
		if(!this.valid) return;
		if(this.changeDetector && !this.changeDetector()){
			await this.cancelEdit();
			return;
		}
		if(!this.confirmTextMaker || !ask){
			await this.onConfirmFinish();
			return;
		}else{
			ask();
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
export { EditableCell } 
export default EditableCell
</script>
<style scoped>
</style>
