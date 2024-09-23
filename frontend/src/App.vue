<template>
    <v-app>
        <v-flex shrink>
            <v-expand-transition appear mode="out-in">
                <top-nav-bar appear :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
            </v-expand-transition>
        </v-flex>
        <side-nav-drawer :drawer="drawer" @update:drawer="toggleDrawer" v-if="isLoggedIn"/>
        <image-background :src="require('@/assets/img/login-background.png')" v-if="showBackground"></image-background>
        <v-main>
            <my-page-transition appear name="overlay-down" class="fill-height">
                <server-down-view appear v-if="!serverReachable" key="a"/>
                <router-view appear v-else :key="$route.matched[0].path"/>
            </my-page-transition>
        </v-main>
        <idle-overlay :idle-wait="300" :logout-wait="300"/>
        <loading-overlay/>
        <dialog-stack :items="tabDialogs" @dialogstackpop="popTabDialog"/>
    </v-app>
</template>

<script>
import { 
    TAuthError, TAuthErrorCode, 
    TLoginError, TLoginErrorCode 
} from "@/rpc/gen/user.auth.errors_types";

import { authStore, appStore, clientStore } from "@/store/stores";
import { router } from '@/router/index';
import { authRouter } from '@/router/routers/auth';
import errorHelper from '@/store/helpers/error';

import { Component, Watch } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';

import {SlideYDownTransition, CollapseTransition} from 'vue2-transitions'
import ImageBackground from '@/components/general/ImageBackground'
import LoadingOverlay from '@/components/overlay/LoadingOverlay';
import SideNavDrawer from '@/components/main/SideNavDrawer';
import TopNavBar from '@/components/main/TopNavBar';
import DialogStack from '@/components/dialog/DialogStack';
import IdleOverlay from '@/components/overlay/IdleOverlay';

import ServerDownView from '@/modules/general/server_down/views/main';
import MyPageTransition from '@/components/general/MyPageTransition';


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
        SlideYDownTransition,
        CollapseTransition,
        MyPageTransition
    }
})
class App extends BaseView{

    drawer = false;
    mounted(){
        appStore.setTabBusy(false);
    }
    get showBackground(){
        return this.serverReachable;
        //return this.serverReachable && !this.isLoggedIn;
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
            router.safePush({ name: "beranda" });
        }
    }

    toggleDrawer(drawer){
        this.drawer = drawer;
    }
    errorCaptured(error, vm, info) {
        return errorHelper.handleUncaughtError(error);
    }
}
export { App }
export default App
</script>
<style>
</style>