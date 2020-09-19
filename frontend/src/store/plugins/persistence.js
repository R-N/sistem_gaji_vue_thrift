import createPersistedState from 'vuex-persistedstate';
import stores from '@/store/stores';
import errorHelper from '@/store/helpers/error';

const storageKey = 'vuex'

const persistencePlugin = createPersistedState({ 
	key: 'keyname',
	storage: window.localStorage,
	paths: [
		'auth.authToken',
		'auth.refreshToken',
		'auth.user',
		'auth.loginDate'
	],
	rehydrated: async store => {
		try{ 
			if (stores.auth.isLoggedIn){
				if (!stores.app.serverReachable){
					stores.client.auth.logout();
				} else {
					if(!await stores.helper.auth.rehydrate()){
						stores.router.auth.dialogSessionExpired();
					}
				}
			}
		}catch(error){
			errorHelper.handleUncaughtError(error);
		}
	}
})
persistencePlugin.storageKey = storageKey;

export { storageKey, persistencePlugin }
export default persistencePlugin