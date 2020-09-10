<template>
	<v-app>
      	<v-flex shrink>
	        <v-expand-transition mode="out-in">
				<top-nav-bar :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
			</v-expand-transition>
		</v-flex>
		<side-nav-drawer :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
		<image-background :src="require('@/assets/img/login-background.png')" v-if="serverReachable && !isLoggedIn"></image-background>
		<v-main>
			<vue-page-transition name="overlay-down" class="fill-height">
				<server-down-view appear v-if="!serverReachable" key="a"/>
				<login-view appear v-else-if="!isLoggedIn" key="b"/>
				<v-container appear 
					class="" 
					align="start"
					justify="start"
					key="c"
					v-else
				>
			        <transition name="fade" mode="out-in">
						<v-row class="" align="start" justify="start"  v-if="serverReachable && isLoggedIn && breadcrumbs">
							<v-col align="start" justify="start">
							    <v-alert
									color="grey"
									text
							    >
						        	<v-breadcrumbs class="py-0" :items="breadcrumbs" large>
										<template v-slot:divider>
											<v-icon>mdi-chevron-right</v-icon>
										</template>
						        	</v-breadcrumbs>
							    </v-alert>
					        </v-col>
					    </v-row>
					</transition>
						<slide-y-down-transition group>
							<router-view appear :key="$route.path"/>
						</slide-y-down-transition>
	      			<v-spacer></v-spacer>
				</v-container>
			</vue-page-transition>
		</v-main>
		<idle-overlay :idle-wait="300" :logout-wait="300"/>
		<loading-overlay/>
		<dialog-stack :items="tabDialogs" @dialogstackpop="popTabDialog"/>
	</v-app>
</template>

<script>

import { authStore, appStore, clientStore } from "@/store/stores";
import { Component, Watch } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';
import ImageBackground from '@/components/ImageBackground'
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

import {SlideYDownTransition, CollapseTransition} from 'vue2-transitions'

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
		ImageBackground,
		LoadingOverlay,
		SideNavDrawer,
		TopNavBar,
		DialogStack,
		IdleOverlay,
		ServerDownView,
		LoginView,
		SlideYDownTransition,
		CollapseTransition
	}
})
class App extends BaseView{

	drawer = false;
	mounted(){
		appStore.setTabBusy(false);
	}
	get breadcrumbs(){
		return appStore.breadcrumbs;
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
