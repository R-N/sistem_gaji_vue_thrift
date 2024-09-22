import TDataPerusahaanService from '@/rpc/gen/TDataPerusahaanService';
import { TUserRole } from '@/rpc/gen/user.user.types_types';
import { TCrudClient } from '@/rpc/client/crud';


class TDataPerusahaanClient extends TCrudClient{
	constructor(stores=null){
		super(
			stores, 
			TDataPerusahaanService, 
			'/api/data/perusahaan',
			{
				fetch: TUserRole.ADMIN_UTAMA,
				create: TUserRole.ADMIN_UTAMA,
				delete: TUserRole.SUPER_ADMIN,
			},
			{
				name: TUserRole.SUPER_ADMIN,
				enabled: TUserRole.ADMIN_UTAMA,
			}
		);
	}
}

const dataPerusahaanClient = new TDataPerusahaanClient();

export { TDataPerusahaanClient, dataPerusahaanClient }
export default dataPerusahaanClient