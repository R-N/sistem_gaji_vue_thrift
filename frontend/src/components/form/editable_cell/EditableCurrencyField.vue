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
            <v-currency-field 
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
import EditableCellTextField from '@/components/form/editable_cell/EditableCellTextField';

@Component({
  	name: "EditableCellCurrencyField",
  	components: {
        EditableCell
  	}
})
class EditableCellCurrencyField extends EditableCellTextField {
}
export { EditableCellCurrencyField } 
export default EditableCellCurrencyField
</script>
<style scoped>
</style>
