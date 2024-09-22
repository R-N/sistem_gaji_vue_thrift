import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";


const name = 'settings'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class SettingsStore extends VuexModule {
    perusahaans = []
    perusahaansDict = {}
    perusahaanId = null

	@MutationAction({ mutate: ['perusahaanId'] })
	async setPerusahaanId(perusahaanId){
		return {
			perusahaanId,
		};
	}

	@MutationAction({ mutate: ['perusahaans', 'perusahaansDict', 'perusahaanId'] })
	async setPerusahaans(perusahaans){
		let perusahaansDict = Object.fromEntries(perusahaans.map(x => [x.id, x.name]));
		let perusahaanId = this.perusahaanId;
		if (!perusahaanId && perusahaans.length > 0){
			perusahaanId = perusahaans[0].id;
		}
		return {
			perusahaans,
			perusahaansDict,
			perusahaanId,
		};
	}
	get perusahaanName(){
		return this.perusahaansDict[this.perusahaanId];
	}
}

const settingsStore = getModule(SettingsStore);

export { name, SettingsStore, settingsStore };
export default settingsStore;