<template>
    <editable-cell 
        @edit="valueEdit = value"
        @finish="emitChange()"
        :change-detector="() => value[itemValue] != valueEdit[itemValue]"
        :confirm-text-maker="() => confirmTextMaker(valueEdit)"
        :parent-busy="parentBusy"
        :disabled="disabled"
    >
        <template v-slot:editing>
            <v-select
                :name="name"
                :items="items"
                :item-title="itemTitle"
                :item-value="itemValue"
                :value="value"
                @change="value => valueEdit = value"
                :disabled="busy || disabled"
            ></v-select>
        </template>
        <template v-slot:default>
            <span>{{ value[itemTitle] }}</span>
        </template>
    </editable-cell>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import EditableCell from '@/components/form/EditableCell';
import WorkingComponent from '@/components/WorkingComponent';

const defaultValue = () => {
    return {"value": 0, "title": ""}
}
@Component({
  	name: "EditableCellSelect",
  	components: {
        EditableCell
  	}
})
class EditableCellSelect extends WorkingComponent {
	@Prop(String) name;
	@Prop([String, Object]) value;
	@Prop([String, Function]) confirmTextMaker; 
	@Prop({ default: false }) disabled;

	@Prop({default: defaultValue}) value;
	@Prop({default: []}) items;
	@Prop({default: "value"}) itemValue;
	@Prop({default: "title"}) itemTitle;

    valueEdit = '';

    mounted(){
    }


	emitChange(){
		this.$emit('change', this.valueEdit);
	}
}
export { EditableCellSelect } 
export default EditableCellSelect
</script>
<style scoped>
</style>
