import { store } from "@/store/index";
import { authStore } from "@/store/modules/auth";
import { clientStore } from "@/store/modules/client";
import { appStore } from "@/store/modules/app";
import { routerStore } from "@/store/modules/router";
import { helperStore } from "@/store/modules/helper";
import { settingsStore } from "@/store/modules/settings";

const stores = { 
	auth: authStore, 
	client: clientStore, 
	app: appStore, 
	router: routerStore,
	helper: helperStore,
	settings: settingsStore,
};
store.modules = stores;

export { store, authStore, clientStore, appStore, routerStore, helperStore, settingsStore };
export default stores;