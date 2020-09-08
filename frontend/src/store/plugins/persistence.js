import createPersistedState from 'vuex-persistedstate';
import { routerStore, clientStore } from '@/store/stores';

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
			if(!await clientStore.auth.rehydrate()){
				routerStore.auth.dialogSessionExpired();
			}
		}catch(error){
			routerStore.auth.dialogUnknownError(error);
		}
	}
})
persistencePlugin.storageKey = storageKey;

export { storageKey, persistencePlugin }
export default persistencePlugin