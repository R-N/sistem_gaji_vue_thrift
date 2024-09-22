import TDataDepartemenService from '@/rpc/gen/TDataDepartemenService';
import { TUserRole } from '@/rpc/gen/user.user.types_types';
import { TCrudClient } from '@/rpc/client/crud';


class TDataDepartemenClient extends TCrudClient{
	constructor(stores=null){
		super(
			stores, 
			TDataDepartemenService, 
			'/api/data/departemen',
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

const dataDepartemenClient = new TDataDepartemenClient();

export { TDataDepartemenClient, dataDepartemenClient }
export default dataDepartemenClient