import createPersistedState from 'vuex-persistedstate'

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
	}
})
persistencePlugin.storageKey = storageKey;

export { storageKey, persistencePlugin }
export default persistencePlugin