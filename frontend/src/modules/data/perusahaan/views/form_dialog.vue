<template>
    <form-dialog
        max-width="400"
        :parent-busy="busy"
        :on-submit="create"
        title="Buat Perusahaan"
        :disabled="disabled"
        :on-reset="reset"
        v-model="myDialog"
    >
        <template v-slot:fields="{ interactable, busy }">
            <v-text-field 
                name="name"
                class="bigger-input" 
                label="Nama" 
                v-model="name" 
                :disabled="!interactable" 
                required
                :rules="nameRules"
                :counter="nameMaxLen"
            />
        </template>
    </form-dialog>
</template>

<script>
import { 
    TPerusahaanError, 
    NAME_MAX_LEN 
} from "@/rpc/gen/data.perusahaan.errors_types";
import { TPerusahaanForm } from "@/rpc/gen/data.perusahaan.structs_types";

import stores from "@/store/stores";
import { NAME_RULES } from '@/modules/data/perusahaan/validator';

import { Component, Prop } from 'vue-property-decorator';
import { FormDialog } from '@/components/form/FormDialog'
import { FormDialogBase } from '@/components/form/FormDialogBase'

@Component({
    name: "DataPerusahaanFormDialog",
    components: {
        FormDialog
    }
})
class DataPerusahaanFormDialog extends FormDialogBase {
    @Prop({ default: false }) disabled;
    name = ''

    nameRules = NAME_RULES

    nameMaxLen = NAME_MAX_LEN

    valid = true;

    reset(){
        this.name = ''
    }

    async create(){
        if(!this.valid) return;
        const view = this;
        view.busy = true;
        let form = new TPerusahaanForm({
            name: this.name
        });
        try{
            let perusahaan = await stores.client.data.perusahaan.create(form);
            view.$emit("create", perusahaan);
            view.close();
        } catch (error) {
            if (stores.helper.error.showFilteredError(error, 
                [TPerusahaanError]
            )) return;
            throw error;
        } finally {
            view.busy = false;
        }
    }
}
export { DataPerusahaanFormDialog }
export default DataPerusahaanFormDialog
</script>

<style scoped>
</style>
