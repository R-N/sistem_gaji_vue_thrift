import { store } from "@/store/stores";
import createMultiTabState from 'vuex-multi-tab-state';

const stateSharePlugin = createMultiTabState({ 
	statesPaths: [
		"auth.authToken",
		"auth.refreshToken",
		"auth.user",
		"app.globalBusy",
		"app.lastUserPresentTime",
		"app.userPresent"
	]
});
stateSharePlugin(store);

export { stateSharePlugin };
export default stateSharePlugin;