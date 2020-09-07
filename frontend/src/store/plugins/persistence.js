import { store, appStore, clientStore } from "@/store/stores";
import createPersistedState from 'vuex-persistedstate'
import { dialogSessionExpired } from '@/router/auth';

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
		if(!await clientStore.auth.rehydrate()){
			dialogSessionExpired();
		}
	}
})
persistencePlugin.storageKey = storageKey;
persistencePlugin(store);

export { storageKey, persistencePlugin }
export default persistencePlugin