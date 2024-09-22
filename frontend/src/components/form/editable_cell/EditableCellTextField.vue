<template>
    <editable-cell 
        :on-reset="() => valueEdit = value"
        :on-finish="finish"
        :change-detector="() => value != valueEdit"
        :confirm-text-maker="() => confirmTextMaker(valueEdit)"
        :parent-busy="busy"
        :disabled="disabled"
        :title="title"
    >
        <template v-slot:editing>
            <v-text-field 
                class="bigger-input"
                :name="name" 
                v-model="valueEdit" 
                :rules="rules"
                :counter="counter"
                :type="type"
                :disabled="busy || disabled"
                :required="required"
                :label="label"
            />
        </template>
        <template v-slot:default>
            <span class="bigger-input">{{ value }}</span>
        </template>
    </editable-cell>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';
import EditableCell from '@/components/form/EditableCell';
import WorkingComponent from '@/components/WorkingComponent';

@Component({
      name: "EditableCellTextField",
      components: {
        EditableCell
      }
})
class EditableCellTextField extends WorkingComponent {
    @Prop(String) title;
    @Prop(String) label;
    @Prop(String) name;
    @Prop(String) type;
    @Prop(String) value;
    @Prop(Number) counter;
    @Prop([String, Function]) confirmTextMaker; 
    @Prop({ default: false }) disabled;
    @Prop([Function, Array]) rules; 
    @Prop({default: true}) required; 
    @Prop(Function) onFinish;

    valueEdit = '';

    finish(){
        this.$emit('change', this.valueEdit);
        if (this.onFinish){
            this.busy = true;
            this.onFinish(this.valueEdit);
            this.busy = false;
        } else{
            this.$emit('finish', this.valueEdit);
        }
    }
}
export { EditableCellTextField } 
export default EditableCellTextField
</script>
<style scoped>
</style>
