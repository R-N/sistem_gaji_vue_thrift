import { store } from "@/store/stores";
import createMultiTabState from 'vuex-multi-tab-state';

const stateSharePlugin = createMultiTabState({ 
	statesPaths: [
		"auth.authToken",
		"auth.refreshToken",
		"auth.user",
		'auth.loginDate',
		"app.globalBusy",
		"app.lastUserPresentTime",
		"app.userPresent",
		"app.globalRefresh",
		"app.globalLogout"
	]
});
stateSharePlugin(store);

export { stateSharePlugin };
export default stateSharePlugin;