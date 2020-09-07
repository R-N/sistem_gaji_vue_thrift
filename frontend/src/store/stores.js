
import { store } from "@/store/index";
import { authStore, requireLogin, requireRole, requireLogout } from "@/store/modules/auth";
import { clientStore } from "@/store/modules/client";
import { appStore } from "@/store/modules/app";

export { store, authStore, clientStore, appStore, requireLogin, requireRole, requireLogout };
export default { store, authStore, clientStore, appStore };