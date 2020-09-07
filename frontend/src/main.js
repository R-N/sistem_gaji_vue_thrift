import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@/assets/css/common.css'
import Vue from 'vue'
import { App } from './App.vue'
import vuetify from './plugins/vuetify';

import { store } from '@/store/index';
import { appStore } from '@/store/modules/app';
import { router } from '@/router/index';

import vueg from 'vueg';
import { setUseHttps, setBackendHost, setBackendPort } from '@/rpc/client/BaseClient';
import { checkBackend, backendUrl } from '@/lib/util';

import VueLazyload from 'vue-lazyload'

Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: 'static/img/error.png',
  loading: 'static/img/loading.gif',
  attempt: 1,
  // the default is ['scroll', 'wheel', 'mousewheel', 'resize', 'animationend', 'transitionend']
  //listenEvents: [ 'scroll' ]
})
Vue.config.productionTip = false;
Vue.use(vueg, router);

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
	appStore.setServerReachable(serverReachable);
	var app = new Vue({
		vuetify,
		store,
		router,
		render: h => h(App)
	}).$mount('#app');
}
import { stores, storePlugins } from '@/store/final';
main();