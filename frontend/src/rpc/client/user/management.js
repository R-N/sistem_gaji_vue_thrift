import TUserManagementService from '@/rpc/gen/TUserManagementService';
import { TCrudClient } from '@/rpc/client/crud';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TUserManagementClient extends TCrudClient{
	constructor(stores=null){
		super(
			stores, 
			TUserManagementService, 
			'/api/user/management',
			{
				fetch: TUserRole.ADMIN_AKUN,
				create: TUserRole.ADMIN_AKUN,
				delete: TUserRole.SUPER_ADMIN,
			},
			{}
		);
	}

	async set_role(id, value){
		await this.set_field("role", id, value, TUserRole.ADMIN_AKUN);
		if (id == this.stores.auth.user.id){
			//await this.stores.auth.setUserRole(new_role);
			await this.stores.client.user.auth.logout();
		}
	}

	async set_email(id, value){
		await this.set_field("email", id, value, TUserRole.ADMIN_AKUN);
		if (id == this.stores.auth.user.id){
			await this.stores.client.user.auth.logout();
		}
	}
	async set_enabled(id, value){
		await this.set_field("enabled", id, value, TUserRole.ADMIN_AKUN);
		if (id == this.stores.auth.user.id && !value){
			await this.stores.client.user.auth.logout();
		}
	}
	async set_password(id, value){
		await this.set_field("password", id, value, TUserRole.SUPER_ADMIN);
		if (id == this.stores.auth.user.id){
			// await this.stores.client.user.auth.logout();
			await this.stores.client.user.auth.login(this.stores.auth.user.username, new_password);
		}
	}
	async set_verified(id, value){
		await this.set_field("verified", id, value, TUserRole.SUPER_ADMIN);
		if (id == this.stores.auth.user.id && !value){
			await this.stores.client.user.auth.logout();
		}
	}
	async delete(id){
		await super.delete(id);
		// this.requireRoleAction("delete");
		// await this.client.delete(this.stores.auth.authToken, id);
		if (id == this.stores.auth.user.id){
			await this.stores.client.user.auth.logout();
		}
	}
}

const userManagementClient = new TUserManagementClient();

export { TUserManagementClient, userManagementClient }
export default userManagementClient