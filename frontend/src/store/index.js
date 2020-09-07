import Vue from "vue";
import 'es6-promise/auto';
import Vuex from "vuex";

import { config } from 'vuex-module-decorators';
// Set rawError to true by default on all @Action decorators
config.rawError = true

Vue.use(Vuex);


const store = new Vuex.Store({
	state: {},
	mutations: {},
	actions: {},
	modules: {},
  	plugins: [],
});
const unregisterModule = (name) => { if(store.name) store.unregisterModule(name) };
export { store, unregisterModule };
export default { store, unregisterModule }
