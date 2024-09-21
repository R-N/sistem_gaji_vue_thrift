import { StoreUser } from '@/store/user';
import { TPerusahaanQuery } from '@/rpc/gen/data.perusahaan.structs_types';

class SettingsHelper extends StoreUser{
	constructor(stores=null){
		super(stores);
	}

	async fetchPerusahaans(){
		this.stores.helper.auth.requireLogin();
		let query = new TPerusahaanQuery({enabled: true});
        let perusahaans = await this.stores.client.data.perusahaan.fetch(query);
        await this.stores.settings.setPerusahaans(perusahaans);
        return perusahaans;
	}

    async getSettings(){
        await this.fetchPerusahaans();
        return true;
    }
}

const settingsHelper = new SettingsHelper();

export { SettingsHelper, settingsHelper }
export default settingsHelper