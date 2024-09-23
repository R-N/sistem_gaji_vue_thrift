<template>
    <v-navigation-drawer
        v-model="syncedDrawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        app
        
    >
        <v-list dense>
            <template v-for="item in items">
                <v-row
                    v-if="item.heading"
                    :key="item.heading"
                    align="center"
                >
                    <v-col cols="6">
                        <v-subheader v-if="item.heading">
                            {{ item.heading }}
                        </v-subheader>
                    </v-col>
                    <v-col
                        cols="6"
                        class="text-center"
                    >
                        <a
                            href="#!"
                            class="body-2 black--text"
                        >EDIT</a>
                    </v-col>
                </v-row>
                <v-list-group
                    v-else-if="item.children"
                    :key="item.text"
                    v-model="item.model"
                    :prepend-icon="item.model ? item.icon : item['icon-alt']"
                    append-icon=""
                >
                    <template v-slot:activator>
                        <v-list-item-content>
                            <v-list-item-title>
                                {{ item.text }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </template>
                    <v-list-item
                        v-for="(child, i) in item.children"
                        :key="i"
                        :to="child.to || '#'"
                        link
                    >
                        <v-list-item-action v-if="child.icon">
                            <v-icon>{{ child.icon }}</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>{{ child.text }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-group>
                <v-list-item
                    v-else
                    :key="item.text"
                    :to="item.to || '#'"
                    link
                >
                    <v-list-item-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>{{ item.text }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </template>
        </v-list>
    </v-navigation-drawer>
</template>
<script>
import { Vue, Component, Prop, PropSync } from 'vue-property-decorator';
import MyComponent from "@/components/MyComponent";

@Component({
    name: "SideNavDrawer"
})
class SideNavDrawer extends MyComponent {
    @PropSync('drawer', { type: Boolean }) syncedDrawer;
    items = [
        { icon: 'mdi-home', text: 'Beranda', to: { name: 'beranda' } },
        {
            icon: 'mdi-chevron-up',
            'icon-alt': 'mdi-chevron-down',
            text: 'Data',
            model: false,
            children: [
                { text: 'Perusahaan', to: { name: 'data-perusahaan' } },
                { text: 'Departemen', to: { name: 'data-departemen' } },
                { text: 'Job Level', to: { name: 'data-job-level' } },
                { text: 'Jabatan', to: { name: 'data-jabatan' } },
                { text: 'Karyawan', to: { name: 'data-karyawan' } },
                { text: 'Shift', to: { name: 'data-shift' } },
            ],
        },
        {
            icon: 'mdi-chevron-up',
            'icon-alt': 'mdi-chevron-down',
            text: 'Gaji',
            model: false,
            children: [
                { text: 'Job Level', to: { name: 'gaji-job-level' } },
                { text: 'Tunjangan Khusus', to: { name: 'gaji-tunjangan-khusus' } },
                { text: 'Karyawan', to: { name: 'gaji-karyawan' } },
                { text: 'Lembur', to: { name: 'gaji-lembur' } },
                { text: 'Absen', to: { name: 'gaji-absen' } },
            ],
        },
        {
            icon: 'mdi-chevron-up',
            'icon-alt': 'mdi-chevron-down',
            text: 'Angsuran',
            model: false,
            children: [
                { text: 'Angsuran', to: { name: 'angsuran-angsuran' } },
                { text: 'Potongan', to: { name: 'angsuran-potongan' } },
            ],
        },
        {
            icon: 'mdi-chevron-up',
            'icon-alt': 'mdi-chevron-down',
            text: 'Laporan',
            model: false,
            children: [
                { text: 'Slip Gaji', to: { name: 'laporan-slip-gaji' } },
                { text: 'Laporan Gaji', to: { name: 'laporan-gaji' } },
                { text: 'Laporan Lembur', to: { name: 'laporan-lembur' } },
                { text: 'Laporan Absen', to: { name: 'laporan-absen' } },
                { text: 'Laporan Angsuran', to: { name: 'laporan-angsuran' } },
                { text: 'Rekap Gaji', to: { name: 'laporan-rekap-gaji' } },
            ],
        },
        {
            icon: 'mdi-chevron-up',
            'icon-alt': 'mdi-chevron-down',
            text: 'Sistem',
            model: false,
            children: [
                { text: 'Variabel', to: { name: 'system-variables' } },
                { text: 'Backup', to: { name: 'backup' } },
                { text: 'Akun', to: { name: 'user-management' } },
            ],
        },
    ];
}
export { SideNavDrawer }
export default SideNavDrawer;
</script>

<style scoped>
</style>