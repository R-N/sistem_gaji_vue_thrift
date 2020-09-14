import { authHelper } from '@/store/helpers/auth';
import { appHelper } from '@/store/helpers/app';

const helpers = {
	auth: authHelper,
	app: appHelper
}

const init = (stores) => {
	Object.keys(helpers).forEach(function(key) {
		helpers[key].init(stores);
	});
}
const initHelpers = init;

export { helpers, init, initHelpers }
export default helpers