<template>
    <v-dialog
        v-model="myDialog"
        max-width="400"
        :persistent="busy"
    >
        <v-card class="">
            <v-form ref="myForm" v-model="valid" @submit.prevent="create" class="p-2" :disabled="!interactable">
                <v-card-title class="headline">Buat Job Level</v-card-title>
                <v-card-text>
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
                    <v-currency-field
                        name="gaji-pokok"
                        class="bigger-input" 
                        label="Gaji Pokok" 
                        v-model="gajiPokok" 
                        :disabled="!interactable" 
                        required
                        :rules="gajiPokokRules"
                        :counter="moneyMaxLen"
                        hide-spin-buttons
                    />
                    <v-currency-field
                        name="tunjangan-jabatan"
                        class="bigger-input" 
                        label="Tunjangan Jabatan" 
                        v-model="tunjanganJabatan" 
                        :disabled="!interactable" 
                        required
                        :rules="tunjanganJabatanRules"
                        :counter="moneyMaxLen"
                        hide-spin-buttons
                    />
                    <v-currency-field
                        name="upah-lembur-1"
                        class="bigger-input" 
                        label="Upah Lembur 1" 
                        v-model="upahLembur1" 
                        :disabled="!interactable" 
                        required
                        :rules="upahLembur1Rules"
                        :counter="moneyMaxLen"
                        hide-spin-buttons
                    />
                    <v-currency-field
                        name="upah-lembur-2"
                        class="bigger-input" 
                        label="Upah Lembur 2" 
                        v-model="upahLembur2" 
                        :disabled="!interactable" 
                        required
                        :rules="upahLembur2Rules"
                        :counter="moneyMaxLen"
                        hide-spin-buttons
                    />
                    <v-currency-field
                        name="upah-lembur-3"
                        class="bigger-input" 
                        label="Upah Lembur 3" 
                        v-model="upahLembur3" 
                        :disabled="!interactable" 
                        required
                        :rules="upahLembur3Rules"
                        :counter="moneyMaxLen"
                        hide-spin-buttons
                    />
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="green darken-1"
                            text
                            @click.stop="close()"
                            :disabled="!interactable"
                        >
                            Batal
                        </v-btn>
                        <v-btn
                            type="submit"
                            color="green darken-1"
                            text
                            :disabled="!interactable"
                            :loading="busy"
                        >
                            Ok
                        </v-btn>
                    </v-card-actions>
                </v-card-text>
            </v-form>
        </v-card>
    </v-dialog>
</template>

<script>
import { TUserRole, T_ROLE_STR } from "@/rpc/gen/user.user.types_types";
import { 
    TJobLevelError, 
    NAME_MAX_LEN,
    MONEY_MAX_LEN,
} from "@/rpc/gen/data.job_level.errors_types";
import { TJobLevelForm } from "@/rpc/gen/data.job_level.structs_types";

import stores from "@/store/stores";
import { 
    NAME_RULES, 
    GAJI_POKOK_RULES, 
    TUNJANGAN_JABATAN_RULES, 
    UPAH_LEMBUR_RULES, 
    UPAH_LEMBUR_RULES_2, 
    UPAH_LEMBUR_1_RULES, 
    UPAH_LEMBUR_2_RULES, 
    UPAH_LEMBUR_3_RULES, 
} from '@/modules/data/job_level/validator';

import { Component, Prop, Watch, Model } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

import CardTitle from '@/components/card/CardTitle'

@Component({
    name: "DataJobLevelFormDialog",
    components: {
        CardTitle,
    }
})
class DataJobLevelFormDialog extends WorkingComponent {
    @Prop({ default: false }) disabled;
    @Model('change', { type: Boolean }) dialog;
    name = ''

    nameRules = NAME_RULES
    gajiPokokRules = GAJI_POKOK_RULES
    tunjanganJabatanRules = TUNJANGAN_JABATAN_RULES
    upahLemburRules = UPAH_LEMBUR_RULES
    upahLemburRules2 = UPAH_LEMBUR_RULES_2
    upahLembur1Rules = UPAH_LEMBUR_1_RULES
    upahLembur2Rules = UPAH_LEMBUR_2_RULES
    upahLembur3Rules = UPAH_LEMBUR_3_RULES

    nameMaxLen = NAME_MAX_LEN
    moneyMaxLen = MONEY_MAX_LEN

    gajiPokok = 0
    tunjanganJabatan = 0
    upahLembur1 = 0
    upahLembur2 = 0
    upahLembur3 = 0

    valid = true;

    @Watch('myDialog')
    onDialogChange(val, oldVal){
        if( this.$refs.myForm){
            this.$refs.myForm.resetValidation();
        }
        this.name = '';
        this.gajiPokok = 0;
        this.tunjanganJabatan = 0;
        this.upahLembur1 = 0;
        this.upahLembur2 = 0;
        this.upahLembur3 = 0;
    }

    close(){
        this.busy = false;
        this.myDialog = false;
    }

    get interactable(){
        return !this.disabled && !this.busy;
    }

    get myDialog(){
        return this.dialog;
    }
    set myDialog(value){
        if(value == this.dialog) return;
        if (!value){
            this.busy = false;
        }
        this.$emit('change', value);
    }

    async create(){
        this.$refs.myForm.validate();
        if(!this.valid) return;
        const view = this;
        view.busy = true;
        let form = new TJobLevelForm({
            name: this.name,
            gaji_pokok: this.gajiPokok,
            tunjangan_jabatan: this.tunjanganJabatan,
            upah_lembur_1: this.upahLembur1,
            upah_lembur_2: this.upahLembur2,
            upah_lembur_3: this.upahLembur3,
        });
        try{
            let jobLevel = await stores.client.data.jobLevel.create(form);
            view.$emit("create", jobLevel);
            view.close();
        } catch (error) {
            if (stores.helper.error.showFilteredError(error, 
                [TJobLevelError]
            )) return;
            throw error;
        } finally {
            view.busy = false;
        }
    }
}
export { DataJobLevelFormDialog }
export default DataJobLevelFormDialog
</script>

<style scoped>
</style>
