import { authRouter } from '@/router/routers/auth';

const init = (stores, router) => {
	authRouter.init(stores, router);
}
const initRouters = init;

const routers = {
	auth: authRouter
}

export { init, initRouters, routers, authRouter }
export default routers