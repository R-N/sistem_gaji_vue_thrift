import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";

const name = 'client'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class ClientStore extends VuexModule {
	user = null;
	hello = null;
	system = null;
	data = null;

	@MutationAction({ mutate: ['hello', 'user', 'system', 'data'] })
	async init(payload){
		return payload;
	}

}
const clientStore = getModule(ClientStore);

export { name, clientStore }
export default clientStore;