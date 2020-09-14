import createMultiTabState from 'vuex-multi-tab-state';

const stateSharePlugin = createMultiTabState({ 
	statesPaths: [
		"auth.authToken",
		"auth.refreshToken",
		"auth.user",
		'auth.loginDate',
		"app.globalBusy",
		"app.authBusy",
		"app.lastUserPresentTime",
		"app.userPresent",
		"app.globalRefresh",
		"app.globalLogout",
		"app.serverReachable"
	]
});

export { stateSharePlugin };
export default stateSharePlugin;