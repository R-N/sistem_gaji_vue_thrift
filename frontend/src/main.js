import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@/assets/css/common.css'
import Vue from 'vue'

import vuetify from './plugins/vuetify';

import vueg from 'vueg';
Vue.use(vueg, router);

import VueLazyload from 'vue-lazyload'
Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: 'static/img/error.png',
  loading: 'static/img/loading.gif',
  attempt: 1
})

import { setUseHttps, setBackendHost, setBackendPort } from '@/rpc/client/base';
import { checkBackend, backendUrl } from '@/lib/util';
import { App } from './App.vue'
import { store, stores, plugins } from '@/store/final';
import { router, routers } from '@/router/final';

import { AuthServiceClient } from '@/rpc/client/auth';
import { HelloServiceClient } from '@/rpc/client/hello';

const clients = {
	auth: new AuthServiceClient(stores),
	hello: new HelloServiceClient(stores)
}
stores.clientStore.init(clients);

routers.init(stores, router);
stores.routerStore.init(routers.forStore);

console.log(store);
plugins.init(store);

Vue.config.productionTip = false;
async function main(){
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