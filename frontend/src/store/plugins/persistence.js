import { store, appStore, clientStore } from "@/store/stores";
import createPersistedState from 'vuex-persistedstate'

const storageKey = 'vuex'

const persistencePlugin = createPersistedState({ 
	key: 'keyname',
	storage: window.localStorage,
	paths: [
		'auth.authToken',
		'auth.refreshToken',
		'auth.user'
	],
	rehydrated: async store => {
		await clientStore.auth.rehydrate();
	}
})
persistencePlugin.storageKey = storageKey;
persistencePlugin(store);

export { storageKey, persistencePlugin }
export default persistencePlugin