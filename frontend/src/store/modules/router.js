import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";

const name = 'rouer'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class RouterStore extends VuexModule {
	auth = null;

	@MutationAction({ mutate: ['auth'] })
	async init(payload){
		return payload;
	}

	get initClients(){
		return (stores, router) => {
			this.auth.init(stores, router);
		}
	}
}
const routerStore = getModule(RouterStore);

export { name, routerStore }
export default routerStore;