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

@Component({
	name: "SideNavDrawer"
})
class SideNavDrawer extends Vue {
	@PropSync('drawer', { type: Boolean }) syncedDrawer;
	items = [
		{ icon: 'mdi-home', text: 'Beranda', to: { name: 'beranda' } },
		{
			icon: 'mdi-chevron-up',
			'icon-alt': 'mdi-chevron-down',
			text: 'Karyawan',
			model: false,
			children: [
				{ text: 'Departemen' },
				{ text: 'Job Level' },
				{ text: 'Jabatan' },
				{ text: 'Karyawan' },
				{ text: 'Shift' },
			],
		},
		{
			icon: 'mdi-chevron-up',
			'icon-alt': 'mdi-chevron-down',
			text: 'Gaji',
			model: false,
			children: [
				{ text: 'Job Level' },
				{ text: 'Tunjangan Khusus' },
				{ text: 'Karyawan' },
				{ text: 'Lembur' },
				{ text: 'Absen' },
			],
		},
		{
			icon: 'mdi-chevron-up',
			'icon-alt': 'mdi-chevron-down',
			text: 'Angsuran',
			model: false,
			children: [
				{ text: 'Angsuran' },
				{ text: 'Potongan' },
			],
		},
		{
			icon: 'mdi-chevron-up',
			'icon-alt': 'mdi-chevron-down',
			text: 'Laporan',
			model: false,
			children: [
				{ text: 'Slip Gaji' },
				{ text: 'Laporan Gaji' },
				{ text: 'Laporan Lembur' },
				{ text: 'Laporan Absen' },
				{ text: 'Laporan Angsuran' },
				{ text: 'Rekap Gaji' },
			],
		},
		{
			icon: 'mdi-chevron-up',
			'icon-alt': 'mdi-chevron-down',
			text: 'Pengaturan',
			model: false,
			children: [
				{ text: 'Variabel' },
				{ text: 'Backup', to: { name: 'backup' } },
				{ text: 'Akun' },
			],
		},
	];
}
export { SideNavDrawer }
export default SideNavDrawer;
</script>

<style scoped>
</style>