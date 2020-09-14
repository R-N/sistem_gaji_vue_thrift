import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";

const name = 'helper'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class HelperStore extends VuexModule {
	auth = null;

	@MutationAction({ mutate: ['auth'] })
	async init(payload){
		return payload;
	}

	get initHelpers(){
		return (stores, router) => {
			this.auth.init(stores, router);
		}
	}
}
const helperStore = getModule(HelperStore);

export { name, helperStore }
export default helperStore;