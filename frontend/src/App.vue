<template>
	<v-app>
      	<v-flex shrink>
	        <v-expand-transition mode="out-in">
				<top-nav-bar :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
			</v-expand-transition>
		</v-flex>
		<side-nav-drawer :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
        <transition name="bounce" mode="out-in">
			<router-view v-transition/>
		</transition>
		<idle-overlay :idle-wait="5" :logout-wait="5"/>
		<loading-overlay/>
		<dialog-stack :items="tabDialogs" @dialogstackpop="popTabDialog"/>
	</v-app>
</template>

<script>

import { authStore, appStore } from "@/store/stores";
import { Component } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';
import LoadingOverlay from '@/components/LoadingOverlay';
import SideNavDrawer from '@/components/SideNavDrawer';
import TopNavBar from '@/components/TopNavBar';
import DialogStack from '@/components/DialogStack';
import IdleOverlay from '@/components/IdleOverlay';
import { router } from '@/router/index';
import { dialogRequireLogin, dialogRequireLogout, dialogRequireRole } from '@/router/auth';
import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";

@Component({
	name: "App",
	components: {
		//'login-view': () => import('./views/LoginView.vue'),
		LoadingOverlay,
		SideNavDrawer,
		TopNavBar,
		DialogStack,
		IdleOverlay
	}
})
class App extends BaseView{

	drawer = false;

	get tabDialogs(){
		return appStore.tabDialogs;
	}

	async popTabDialog(){
		await appStore.popTabDialog();
	}

	get isLoggedIn(){
		return authStore.isLoggedIn;
	}

	toggleDrawer(drawer){
		this.drawer = drawer;
	}
	errorCaptured(error, vm, info) {
		if (error instanceof LoginError && error.code === LoginErrorCode.ALREADY_LOGGED_IN){
			return dialogRequireLogout();
		}
		if (error instanceof AuthError){
			if (error.code === AuthErrorCode.INVALID_ROLE){
				return dialogRequireRole();
			} else if (error.code === AuthErrorCode.NOT_LOGGED_IN){
				return dialogRequireLogin();
			}
		}
	}
}
export { App }
export default App
</script>
