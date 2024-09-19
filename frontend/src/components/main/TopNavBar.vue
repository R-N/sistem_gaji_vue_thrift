<template>
	<v-app-bar
		:clipped-left="$vuetify.breakpoint.lgAndUp"
		app
		color="primary"
		dark
	>
		<v-app-bar-nav-icon @click.stop="syncedDrawer = !syncedDrawer"></v-app-bar-nav-icon>
		<v-toolbar-title
			style="width: 300px"
			class="ml-0 pl-4"
		>
			<span class="hidden-sm-and-down">Sistem Gaji {{ perusahaanNama }}</span>
		</v-toolbar-title>
		<v-spacer></v-spacer>
		<v-menu
			bottom
			left
			close-on-click
			offset-y
		>
			<template v-slot:activator="{ on, attrs }">
				<v-btn 
					icon
					v-bind="attrs"
					v-on="on"
				>
			        <v-badge
						overlap
						color="green"
						:content="notifCount"
						:value="notifCount"
			        >
						<v-icon>mdi-bell</v-icon>
			        </v-badge>
				</v-btn>
			</template>

			<v-list>
				<v-list-item
					v-for="(notif, i) in notifs"
					:key="i"
					@click=""
				>
					<v-list-item-title>{{ notif.text }}</v-list-item-title>
				</v-list-item>
			</v-list>
		</v-menu>
		<v-menu
			bottom
			left
			close-on-click
			offset-y
		>
			<template v-slot:activator="{ on, attrs }">
				<v-btn
					text
					rounded
					large
					v-bind="attrs"
					v-on="on"
				>
					<v-avatar
						size="32px"
						item
					>
						<v-icon size="32px">mdi-account</v-icon>
					</v-avatar>
					<span class="ml-2" v-if="userName">{{ userName }}</span>
				</v-btn>
			</template>

			<v-list>
				<v-list-item :to="{ name: 'profil' }">
					<v-list-item-title>Profil</v-list-item-title>
				</v-list-item>
				<v-list-item @click="logout">
					<v-list-item-title>Logout</v-list-item-title>
				</v-list-item>
			</v-list>
		</v-menu>
	</v-app-bar>
</template>
<script>
import { authStore, clientStore, appStore, settingsStore } from "@/store/stores";

import { Vue, Component, Prop, PropSync } from 'vue-property-decorator';

@Component({
	name: "TopNavBar"
})
class TopNavBar extends Vue {
	@PropSync('drawer', { type: Boolean }) syncedDrawer;
	notifs = [
		{ text: 'Notif 1' },
		{ text: 'Notif 2' }
	]
	get notifCount(){
		return this.notifs.length;
	}
	get userName(){
		if (authStore.authToken && authStore.user) return authStore.user.name;
		return '';
	}
	get perusahaanNama(){
		return settingsStore.perusahaanNama;
	}
	async logout(){
		const view = this;
		view.globalBusy = true;
		try{
			await clientStore.user.auth.logout();
		} catch (error){
			console.log(error);
		} finally {
			view.globalBusy = false;
		}
	}
}
export { TopNavBar }
export default TopNavBar

</script>

<style scoped>
</style>