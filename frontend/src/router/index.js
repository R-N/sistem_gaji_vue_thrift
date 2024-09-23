import Vue from 'vue';
import VueRouter from 'vue-router';

import { appStore } from "@/store/stores";

import MainView from '@/views/MainView';

import NotFoundView from '@/modules/general/not_found/views/main';
import LoginView from '@/modules/auth/login/views/main';

// import BerandaView from '@/modules/general/beranda/views/main';
//import ProfilView from '@/modules/user/profile/views/main';

import systemRoutes from '@/modules/system/routes';
import emailRoutes from '@/modules/email/routes';
import dataRoutes from '@/modules/data/routes';
import gajiRoutes from '@/modules/gaji/routes';
import angsuranRoutes from '@/modules/angsuran/routes';
import laporanRoutes from '@/modules/laporan/routes';
import userRoutes from '@/modules/user/routes';
import generalRoutes from '@/modules/general/routes';

const routes = [
    //{ path: '/login', component: LoginView, name: "login" },
    ...emailRoutes,
    { path: '/', component: MainView, name: "main",
        children: [
            ...dataRoutes,
            ...gajiRoutes,
            ...angsuranRoutes,
            ...laporanRoutes,
            ...systemRoutes,
            ...userRoutes,
            ...generalRoutes,
            //{ path: 'profil', component: ProfilView, name: "profil" },
            // { path: '', component: BerandaView, name: "beranda" },
        ] 
    },
    { path: '*', component: NotFoundView, name: "not-found" }
]
const router = new VueRouter({
    mode: 'history',
    routes // short for `routes: routes`
})

router.afterEach((to, from) => {
    appStore.setRouterBusy(false);
    appStore.setRouteValid(true);
})
router.beforeEach((to, from, next) => {
    appStore.setRouterBusy(true);
    next();
})

Vue.use(VueRouter);

const safeRouterPush = async (route) => {
    await appStore.setRouterBusy(false);
    if ((!route.path || route.path != router.currentRoute.path)
         && (!route.name || route.name != router.currentRoute.name)){
        return await router.push(route);
    }
}
router.safePush = safeRouterPush;

export { routes, router, safeRouterPush }
export default { routes, router }