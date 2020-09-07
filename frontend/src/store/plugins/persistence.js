import { store, appStore, clientStore } from "@/store/stores";
import createPersistedState from 'vuex-persistedstate'
import { dialogSessionExpired, dialogUnknownError } from '@/router/auth';

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
			if(!await clientStore.auth.rehydrate()){
				dialogSessionExpired();
			}
		}catch(error){
			dialogUnknownError(error);
		}
	}
})
persistencePlugin.storageKey = storageKey;
persistencePlugin(store);

export { storageKey, persistencePlugin }
export default persistencePlugin