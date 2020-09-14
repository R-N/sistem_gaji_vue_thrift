import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@/assets/css/common.css'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import 'vue2-animate/dist/vue2-animate.min.css'
//import 'paper-css/paper.css'
import Vue from 'vue'

import vuetify from './plugins/vuetify';
/*
import vueg from 'vueg';
Vue.use(vueg, router);
*/

import VuePageTransition from 'vue-page-transition'

Vue.use(VuePageTransition)

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
import { store, stores } from '@/store/final';
import { initStorePlugins } from '@/store/plugins';
import { router, routers } from '@/router/final';
import { initRouters } from '@/router/routers';

import { clients, initClients } from '@/rpc/clients';
import { helpers, initHelpers } from '@/store/helpers';

Vue.config.productionTip = false;
async function main(){
	initClients(stores);
	await stores.client.init(clients);

	initRouters(stores, router);
	await stores.router.init(routers);

	initHelpers(stores, router);
	await stores.helper.init(helpers);

	initStorePlugins(store);

	const serverHost = backendUrl(defaultUseHttps, defaultBackendHost, defaultBackendPort);
	var serverReachable = false;
	var backendInfo = null;
	try{
		backendInfo = await checkBackend(serverHost + "/backend");
		serverReachable = true;
	}catch(error){
		console.log("Server unreachable");
	}
	stores.app.setServerReachable(serverReachable);
	var app = new Vue({
		vuetify,
		store,
		router,
		render: h => h(App)
	}).$mount('#app');
}
main();