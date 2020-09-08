
import { store } from "@/store/index";
import { authStore, requireLogin, requireRole, requireLogout } from "@/store/modules/auth";
import { clientStore } from "@/store/modules/client";
import { appStore } from "@/store/modules/app";
import { routerStore } from "@/store/modules/router";

export { store, authStore, clientStore, appStore, routerStore, requireLogin, requireRole, requireLogout };
export default { store, authStore, clientStore, appStore, routerStore };