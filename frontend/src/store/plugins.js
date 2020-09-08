import { storageKey, persistencePlugin } from '@/store/plugins/persistence';
import { stateSharePlugin } from '@/store/plugins/state_share';

const init = (store) => {
	persistencePlugin(store);
	stateSharePlugin(store);
}
const initStorePlugins = init;

export { storageKey, persistencePlugin, stateSharePlugin, init, initStorePlugins }
export default { persistencePlugin, stateSharePlugin, init }