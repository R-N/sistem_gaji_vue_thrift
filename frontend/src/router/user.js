import { StoreUser } from '@/store/user';

class RouterUser extends StoreUser{
	constructor(stores=null, router=null){
		super(stores);
		this.init(null, router);
	}

	init(stores, router){
		if (stores) super.init(stores);
		if (router) this.router = router;
		console.log(router);
		return this;
	}
}

export { RouterUser }

export default RouterUser;