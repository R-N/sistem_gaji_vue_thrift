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
	auth = null;
	hello = null;
	user = null;
	backup = null;

	@MutationAction({ mutate: ['auth', 'hello', 'user', 'backup'] })
	async init(payload){
		return payload;
	}

	get initClients(){
		return (stores) => {
			this.auth.init(stores);
			this.hello.init(stores);
		}
	}
}
const clientStore = getModule(ClientStore);

export { name, clientStore }
export default clientStore;