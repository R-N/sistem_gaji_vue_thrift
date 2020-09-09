import createPersistedState from 'vuex-persistedstate';
import { routerStore, clientStore, authStore, appStore, } from '@/store/stores';

const storageKey = 'vuex'
console.log(routerStore);
console.log(clientStore);

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
			if (authStore.isLoggedIn){
				if (!appStore.serverReachable){
					clientStore.auth.logout();
				} else {
					if(!await clientStore.auth.rehydrate()){
						routerStore.auth.dialogSessionExpired();
					}
				}
			}
		}catch(error){
			routerStore.auth.dialogUnknownError(error);
		}
	}
})
persistencePlugin.storageKey = storageKey;

export { storageKey, persistencePlugin }
export default persistencePlugin