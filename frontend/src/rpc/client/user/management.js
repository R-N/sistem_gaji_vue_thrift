import TUserManagementService from '@/rpc/gen/TUserManagementService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TUserManagementClient extends TBaseClient{
	constructor(stores=null){
		super(stores, TUserManagementService, '/api/user/management');
	}

	async fetch_akun(query){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		return await this.client.fetch_akun(this.stores.auth.authToken, query);
	}
	async register_akun(form){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		return await this.client.register_akun(this.stores.auth.authToken, form);
	}

	async set_role(user_id, new_role){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		await this.client.set_role(this.stores.auth.authToken, user_id, new_role);
		if (user_id == this.stores.auth.user.id){
			//await this.stores.auth.setUserRole(new_role);
			await this.stores.client.user.auth.logout();
		}
	}

	async set_email(user_id, new_email){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		await this.client.set_email(this.stores.auth.authToken, user_id, new_email);
	}
	async set_password(user_id, new_password){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		await this.client.set_password(this.stores.auth.authToken, user_id, new_password);
		if (user_id == this.stores.auth.user.id){
			await this.stores.client.user.auth.login(this.stores.auth.user.username, new_password);
		}
	}
	async set_enabled(user_id, new_enabled){
		this.stores.helper.auth.requireRole(TUserRole.ADMIN_AKUN);
		await this.client.set_enabled(this.stores.auth.authToken, user_id, new_enabled);
		if (user_id == this.stores.auth.user.id && !new_enabled){
			await this.stores.client.user.auth.logout();
		}
	}
	async set_verified(user_id, new_verified){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.set_verified(this.stores.auth.authToken, user_id, new_verified);
		if (user_id == this.stores.auth.user.id && !new_verified){
			await this.stores.client.user.auth.logout();
		}
	}
	async delete(user_id){
		this.stores.helper.auth.requireRole(TUserRole.SUPER_ADMIN);
		await this.client.delete(this.stores.auth.authToken, user_id);
		if (user_id == this.stores.auth.user.id){
			await this.stores.client.user.auth.logout();
		}
	}
}

const userManagementClient = new TUserManagementClient();

export { TUserManagementClient, userManagementClient }
export default userManagementClient