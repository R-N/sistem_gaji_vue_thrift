<template>
    <base-crud-view 
        title="Perusahaan"
        :create="() => createDialog=true"
        :fetch="fetch"
        create-text="Buat Akun"
        v-model:search="search"
    >
        <template v-slot:default>
            <v-data-table
                class="backup-table"
                :headers="headers"
                :items="items"
                item-key="id"
                :search="search"
                :loading="busy"
            >
                <template v-slot:item.name="{ item }">
                    <editable-cell-text-field
                        name="name"
                        :counter="nameMaxLen"
                        :confirm-text-maker="(value) => setFieldConfirmText('name', item, value)"
                        :value="item.name" 
                        :on-finish="(value) => setName(item, value)"
                        :rules="nameRules"
                        :disabled="!isSuperAdmin || busy"
                    />
                </template>
                <template v-slot:item.enabled="{ item }">
                    <sync-checkbox 
                        :input-value="item.enabled" 
                        :on-change="value => setEnabled(item, value)"
                        :confirm-text-maker="() => setEnabledConfirmText(item)"
                        readonly
                        textDisable="Nonaktifkan"
                        textEnable="Aktifkan"
                        :disabled="!isSuperAdmin || busy"
                    />
                </template>
            </v-data-table>
            <data-perusahaan-form-dialog
                v-model="createDialog"
                @create="addItem"
                :parent-busy="busy"
            />
        </template>
    </base-crud-view>
</template>

<script>
import { TUserRole } from "@/rpc/gen/user.user.types_types";
import { 
    TPerusahaanError, 
    NAME_MAX_LEN 
} from "@/rpc/gen/data.perusahaan.errors_types";
import { TPerusahaanQuery } from '@/rpc/gen/data.perusahaan.structs_types';

import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { NAME_RULES } from '@/modules/data/perusahaan/validator';

import { Component } from 'vue-property-decorator';

import MainCard from '@/components/card/MainCard';
import SyncCheckbox from '@/components/checkbox/SyncCheckbox';

import DataPerusahaanFormDialog from '@/modules/data/perusahaan/views/form_dialog';
import { BaseCrudView } from '@/views/BaseCrudView';
import { BaseCrudViewBase } from '@/views/BaseCrudViewBase';
import EditableCellTextField from '@/components/form/editable_cell/EditableCellTextField';

@Component({
    name: "DataPerusahaanView",
    components: {
        MainCard,
        SyncCheckbox,
        DataPerusahaanFormDialog,
        BaseCrudView,
        EditableCellTextField
    },
    beforeRouteEnter: authRouter.routeRequireRoleNow(TUserRole.SUPER_ADMIN)
})
class DataPerusahaanView extends BaseCrudViewBase {
    createDialog = false;
    nameMaxLen = NAME_MAX_LEN
    nameRules = NAME_RULES

    get nameField(){ return "name"; }
    get itemName(){ return 'Perusahaan'; }
    get client(){ return stores.client.data.perusahaan; }
    get query(){ return new TPerusahaanQuery(); }
    get breadcrumbs(){
        return [
            { text: "Beranda", to: { name: 'beranda' }, exact: true },
            { text: "Data" },
            { text: "Perusahaan" },
        ]
    }
    get headers(){
        let headers = [
            { text: 'Nama', value: 'name' },
            { text: 'Aktif', value: 'enabled', align: 'center' }
        ]
        return headers;
    }
    get filteredErrors() { return [TPerusahaanError]; }
}
export { DataPerusahaanView } 
export default DataPerusahaanView
</script>
<style scoped>
</style>
