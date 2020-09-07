import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";
import { AuthServiceClient } from "@/rpc/client/AuthServiceClient";
import { HelloServiceClient } from "@/rpc/client/HelloServiceClient";

const name = 'client'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class ClientStore extends VuexModule {
	auth = new AuthServiceClient();
	hello = new HelloServiceClient();
}
const clientStore = getModule(ClientStore);

export { name, clientStore }
export default clientStore;