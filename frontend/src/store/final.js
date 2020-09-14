import { store } from '@/store/index';
import stores from '@/store/stores';
import plugins from '@/store/plugins';
import helpers from '@/store/helpers';
import StoreUser from '@/store/user';

const storePlugins = plugins;
const storeHelpers = helpers;
export { store, stores, plugins, storePlugins, helpers, storeHelpers }
export default { store, stores, plugins, helpers }