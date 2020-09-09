import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@/assets/css/common.css'
//import 'paper-css/paper.css'
import Vue from 'vue'

import vuetify from './plugins/vuetify';

import vueg from 'vueg';
Vue.use(vueg, router);

import VueLazyload from 'vue-lazyload'
Vue.use(VueLazyload, {
  preLoad: 1.3,
  //error: 'static/img/error.png',
  //loading: 'static/img/loading.gif',
  attempt: 1
})
// TODO: add loading & error placeholder... maybe

import { setUseHttps, setBackendHost, setBackendPort } from '@/rpc/client/base';
import { checkBackend, backendUrl } from '@/lib/util';
import { App } from './App.vue'
import { store, stores, plugins } from '@/store/final';
import { router, routers } from '@/router/final';

import { TAuthServiceClient } from '@/rpc/client/auth';
import { TUserServiceClient } from '@/rpc/client/user';
import { THelloServiceClient } from '@/rpc/client/hello';
import { TBackupServiceClient } from '@/rpc/client/backup';

const clients = {
	auth: new TAuthServiceClient(stores),
	hello: new THelloServiceClient(stores),
	user: new TUserServiceClient(stores),
	backup: new TBackupServiceClient(stores)
}

Vue.config.productionTip = false;
async function main(){
	await stores.clientStore.init(clients);

	console.log(router);
	routers.init(stores, router);
	await stores.routerStore.init(routers.forStore);

	plugins.init(store);

	const serverHost = backendUrl(defaultUseHttps, defaultBackendHost, defaultBackendPort);
	var serverReachable = false;
	var backendInfo = null;
	try{
		backendInfo = await checkBackend(serverHost + "/backend");
		serverReachable = true;
	}catch(error){
		console.log("Server unreachable");
	}
	stores.appStore.setServerReachable(serverReachable);
	var app = new Vue({
		vuetify,
		store,
		router,
		render: h => h(App)
	}).$mount('#app');
}
main();