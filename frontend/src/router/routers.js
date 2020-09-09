import { authRouter } from '@/router/routers/auth';

const init = (stores, router) => {
	console.log(router);
	authRouter.init(stores, router);
}
const initRouters = init;

const forStore = {
	auth: authRouter
}

export { authRouter, init, initRouters, forStore }
export default { authRouter, init, forStore }