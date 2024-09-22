
<script>

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';
import { BaseView } from '@/views/BaseView';

@Component({
    name: "DialogBase",
    components: {
    }
})
class DialogBase extends BaseView {
    @Model('change', { type: [Boolean, String, Object, Array] }) dialog;
    valid = true;

    async _close(){
        if(this.onCancel){
            this.busy = true;
            await this.onCancel(this.myDialog, this.releaseBusy);
        }else{
            this.$emit("cancel", this.myDialog, this.releaseBusy);
        }
        if (typeof this.myDialog == "boolean" || this.myDialog instanceof Boolean){
            this.myDialog = false;
        }else if (typeof this.myDialog == "string" || this.myDialog instanceof String){
            this.myDialog = '';
        }else if (this.myDialog instanceof Object){
            this.myDialog = null;
        }else if (this.myDialog instanceof Array){
            this.myDialog.pop();
        }else{
            console.log(this.myDialog);
        }
        if (this.reset)
            this.reset();
        this.busy = false;
    }
    async close(){
        return await this._close();
    }

    getForm(){
        return this.$refs.myForm;
    }
    _getValue(){
        let val = this.getForm();
        if (!val)
            val = this.$event;
        return val;
    }
    getValue(){
        return this._getValue();
    }
    _validate(){
        if(this.getForm()){
            this.getForm().validate();
        }
        if(this.onValidate)
            this.onValidate(this.getForm());
        else
            this.$emit('validate', this.getForm());
        return true;
    }
    validate(){
        return this._validate();
    }
    _resetValidation(){
        if(this.getForm()){
            this.getForm().resetValidation();
        }
        this.valid = true;
    }
    resetValidation(){
        return this._resetValidation();
    }
    _reset(){
        this.resetValidation();
        if(this.onReset)
            this.onReset(this.getForm());
        else
            this.$emit('reset', this.getForm());
    }
    reset(){
        this._reset();
    }

    get myDialog(){
        return this.dialog;
    }
    set myDialog(value){
        if(value == this.dialog) return;
        this.reset();
        this.busy = false;
        this.$emit('change', value);
    }

    get interactable(){
        return !this.disabled && !this.busy;
    }
    
    async _submit(){
        this.validate();
        if(!this.valid) return;
        if(this.onSubmit){
            this.busy = true;
            await this.onSubmit(this.getValue());
        }else{
            this.$emit('submit', this.getValue());
        }
        this.close();
    }
    async submit(){
        return await this._submit();
    }
}
export { DialogBase }
export default DialogBase
</script>
