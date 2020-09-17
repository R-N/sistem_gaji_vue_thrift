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
	akun = null;
	auth = null;
	hello = null;
	user = null;
	backup = null;
	email = null;

	@MutationAction({ mutate: ['akun', 'auth', 'hello', 'user', 'backup', 'email'] })
	async init(payload){
		return payload;
	}

}
const clientStore = getModule(ClientStore);

export { name, clientStore }
export default clientStore;