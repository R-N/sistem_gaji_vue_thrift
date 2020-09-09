<template>
	<v-app>
      	<v-flex shrink>
	        <v-expand-transition mode="out-in">
				<top-nav-bar :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
			</v-expand-transition>
		</v-flex>
		<side-nav-drawer :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
        <transition name="fade" mode="out-in">
			<server-down-view v-transition v-if="!serverReachable"/>
			<login-view v-transition v-else-if="!isLoggedIn"/>
			<router-view v-transition v-else />
		</transition>
		<idle-overlay :idle-wait="300" :logout-wait="300"/>
		<loading-overlay/>
		<dialog-stack :items="tabDialogs" @dialogstackpop="popTabDialog"/>
	</v-app>
</template>

<script>

import { authStore, appStore, clientStore } from "@/store/stores";
import { Component, Watch } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';
import LoadingOverlay from '@/components/LoadingOverlay';
import SideNavDrawer from '@/components/SideNavDrawer';
import TopNavBar from '@/components/TopNavBar';
import DialogStack from '@/components/DialogStack';
import IdleOverlay from '@/components/IdleOverlay';
import ServerDownView from '@/views/ServerDownView';
import LoginView from '@/views/LoginView';
import { router } from '@/router/index';
import { authRouter } from '@/router/routers/auth';
import { TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from "@/rpc/gen/auth_types";

const dialogAuthExpired = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Sesi kecil kadaluarsa. Tolong coba lagi, refresh halaman, login ulang, atau laporkan bug."
	});
	return false;
}

@Component({
	name: "App",
	components: {
		//'login-view': () => import('./views/LoginView.vue'),
		LoadingOverlay,
		SideNavDrawer,
		TopNavBar,
		DialogStack,
		IdleOverlay,
		ServerDownView,
		LoginView
	}
})
class App extends BaseView{

	drawer = false;
	mounted(){
		appStore.setTabBusy(false);
	}
	get tabDialogs(){
		return appStore.tabDialogs;
	}

	async popTabDialog(){
		await appStore.popTabDialog();
	}

	get isLoggedIn(){
		return authStore.isLoggedIn;
	}
	get globalRefresh(){
		return appStore.globalRefresh;
	}
	get globalLogout(){
		return appStore.globalLogout;
	}
	get serverReachable(){
		return appStore.serverReachable;
	}

	@Watch('globalRefresh')
	onGlobalRefreshFlagSet(val, oldVal){
		if(val){
			appStore.setRouterBusy(true);
			appStore.setGlobalRefresh(false);
			window.location.reload();
		}
	}


	@Watch('globalLogout')
	onGlobalLogoutFlagSet(val, oldVal){
		if(val){
			appStore.setGlobalLogout(false);
			this.$router.push({ name: "login" });
		}
	}

	toggleDrawer(drawer){
		this.drawer = drawer;
	}
	errorCaptured(error, vm, info) {
		if (error instanceof TLoginError){
			if (error.code === TLoginErrorCode.ALREADY_LOGGED_IN){
				return authRouter.dialogRequireLogout();
			} else if (error.code === TLoginErrorCode.REFRESH_TOKEN_EXPIRED){
				clientStore.auth.logout();
				return authRouter.dialogSessionExpired();
			} else {
				return authRouter.dialogUnknownTAuthError("TLoginError", error.code);
			}
		} else if (error instanceof TAuthError){
			if (error.code === TAuthErrorCode.INVALID_ROLE){
				return authRouter.dialogRequireRole();
			} else if (error.code === TAuthErrorCode.NOT_LOGGED_IN){
				clientStore.auth.logout();
				return authRouter.dialogRequireLogin();
			} else if (error.code === TAuthErrorCode.AUTH_TOKEN_EXPIRED){
				clientStore.auth.logout();
				return authRouter.dialogAuthExpired();
			} else {
				clientStore.auth.logout();
				return authRouter.dialogUnknownTAuthError("TAuthError", error.code);
			}
		} else {
			authRouter.dialogUnknownError(error);
		}
	}
}
export { App }
export default App
</script>
