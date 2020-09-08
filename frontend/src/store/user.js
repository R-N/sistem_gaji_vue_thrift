class StoreUser{
	constructor(stores){
		this.init(stores);
	}

	init(stores){
		if(!stores) return;
		this.stores = stores;
		this.authStore = stores.authStore;
		this.appStore = stores.appStore;
		this.clientStore = stores.clientStore;
		return this;
	}
}

export { StoreUser }
export default StoreUser;