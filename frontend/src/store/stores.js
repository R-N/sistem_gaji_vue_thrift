
import { store } from "@/store/index";
import { authStore } from "@/store/modules/auth";
import { clientStore } from "@/store/modules/client";
import { appStore } from "@/store/modules/app";
import { routerStore } from "@/store/modules/router";

const stores = { store, authStore, clientStore, appStore, routerStore };
store.modules = stores;

export { store, authStore, clientStore, appStore, routerStore };
export default stores;