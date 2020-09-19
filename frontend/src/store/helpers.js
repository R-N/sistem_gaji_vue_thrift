import { authHelper } from '@/store/helpers/auth';
import { errorHelper } from '@/store/helpers/error';

const helpers = {
	auth: authHelper,
	error: errorHelper
}

const init = (stores) => {
	Object.keys(helpers).forEach(function(key) {
		helpers[key].init(stores);
	});
}
const initHelpers = init;

export { helpers, init, initHelpers }
export default helpers