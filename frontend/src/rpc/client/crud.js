import TDataPerusahaanService from '@/rpc/gen/TDataPerusahaanService';
import { TBaseClient } from '@/rpc/client/base';
import { TUserRole } from '@/rpc/gen/user.user.types_types';


class TCrudClient extends TBaseClient{
	constructor(
		stores,
		clientClass, 
		endpoint,
        calls={},
        setters={},
		useHttps=null,
		backendHost=null,
		backendPort=null
	){
		super(stores, clientClass, endpoint, useHttps, backendHost, backendPort);
        this.calls = calls;
        this.setters = setters;
        this.createSetters(setters);
	}

    createSetters(setters){
        this.setters = setters;

        for (const [field, required_role] of Object.entries(this.setters)) {
            this[`set_${field}`] = (id, new_value) => this.set_field(field, id, new_value, required_role);
        }
    }

    getRequiredRoleCall(action){
        if (!this.calls || !(action in this.calls)) throw new Exception("Not implemented");
        return this.calls[action];
    }
    requireRoleCall(action){
        let requiredRole = this.getRequiredRoleCall(action);
        if (requiredRole)
            this.stores.helper.auth.requireRole(requiredRole);
    }

    getRequiredRoleSetter(field){
        if (!this.setters || !(field in this.setters)) throw new Exception("Not implemented");
        return this.setters[field];
    }
    requireRoleSetter(field){
        let requiredRole = this.getRequiredRoleSetter(field);
        if (requiredRole)
            this.stores.helper.auth.requireRole(requiredRole);
    }

	async fetch(query=null){
		this.requireRoleCall("fetch");
		return await this.client.fetch(this.stores.auth.authToken, query);
	}
	async get(id){
		this.requireRoleCall("get");
		return await this.client.get(this.stores.auth.authToken, id);
	}
	async delete(id){
		this.requireRoleCall("delete");
		return await this.client.delete(this.stores.auth.authToken, id);
	}
	async create(form){
		this.requireRoleCall("create");
		return await this.client.create(this.stores.auth.authToken, form);
	}
	async call(action, value, required_role=null){
        if(required_role)
		    this.stores.helper.auth.requireRole(required_role);
        else
            this.requireRoleCall(action);
		await this.client[action](this.stores.auth.authToken, value);
	}
	async set_field(field, id, new_value, required_role=null){
        if(required_role)
		    this.stores.helper.auth.requireRole(required_role);
        else
            this.requireRoleSetter(field);
		await this.client[`set_${field}`](this.stores.auth.authToken, id, new_value);
	}
}

export { TCrudClient }
export default TCrudClient