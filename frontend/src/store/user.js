class StoreUser{
	constructor(stores){
		this.init(stores);
	}

	init(stores){
		if(!stores) return;
		this.stores = stores;
		return this;
	}
}

export { StoreUser }
export default StoreUser;