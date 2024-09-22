<template>
    <editable-cell 
        :on-reset="() => valueEdit = value"
        :on-finish="finish"
        :change-detector="() => value[itemValue] != valueEdit[itemValue]"
        :confirm-text-maker="() => confirmTextMaker(valueEdit)"
        :parent-busy="busy"
        :disabled="disabled"
        :title="title"
    >
        <template v-slot:editing>
            <v-select
                class="bigger-input"
                :label="label"
                :name="name"
                :items="items"
                :item-title="itemTitle"
                :item-value="itemValue"
                :value="value"
                :on-change="value => valueEdit = value"
                :disabled="busy || disabled"
            />
        </template>
        <template v-slot:default>
            <span class="bigger-input">{{ value[itemTitle] }}</span>
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
    @Prop(String) label;
    @Prop(String) title;
    @Prop(String) name;
    @Prop([String, Object]) value;
    @Prop([String, Function]) confirmTextMaker; 
    @Prop({ default: false }) disabled;

    @Prop({default: defaultValue}) value;
    @Prop({default: []}) items;
    @Prop({default: "value"}) itemValue;
    @Prop({default: "title"}) itemTitle;
    @Prop(Function) onFinish;

    valueEdit = '';

    finish(){
        this.$emit('change', this.valueEdit);
        if (this.onFinish){
            this.busy = true;
            this.onFinish(this.valueEdit, this.releaseBusy);
            this.busy = false;
        } else{
            this.$emit('finish', this.valueEdit, this.releaseBusy);
        }
    }
}
export { EditableCellSelect } 
export default EditableCellSelect
</script>
<style scoped>
</style>
