import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@/assets/css/common.css'
import Vue from 'vue'
import { App } from './App.vue'
import vuetify from './plugins/vuetify';

import { stores, storePlugins } from '@/store/final';
import { router } from '@/router/index';

import vueg from 'vueg';

Vue.config.productionTip = false
Vue.use(vueg, router);

var app = new Vue({
	vuetify,
	store: stores.store,
	router,
	render: h => h(App)
}).$mount('#app');

export { app, App }
export default { app, App };