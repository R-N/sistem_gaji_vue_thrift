import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";
import { 
	TAuthError, TAuthErrorCode, 
	TLoginError, TLoginErrorCode 
} from '@/rpc/gen/user.auth.errors_types';
import { TUserRole, T_ROLE_DOUBLES } from '@/rpc/gen/user.user.types_types';

import { dateAsInt } from '@/lib/util';


const name = 'auth'
unregisterModule(name);

@Module({
	namespaced: true,
	name,
	store,
	dynamic: true
})
class AuthStore extends VuexModule {
	authToken = null
	refreshToken = null
	user = null
	authRefresher = null
	loginDate = 0

	@MutationAction({ mutate: ['authToken', 'refreshToken', 'loginDate'] })
	async setTokens(loginResult){
		var refreshToken = loginResult.refresh_token || this.state.refreshToken
		return {
			authToken: loginResult.auth_token,
			refreshToken,
			loginDate: dateAsInt(new Date())
		};
	}

	@MutationAction({ mutate: ['authToken', 'refreshToken', 'loginDate', 'authRefresher', 'user'] })
	async logout(){
		if (this.state.authRefresher) {
			try{
				window.clearInterval(this.state.authRefresher);
			}catch(error){}
		}
		return {
			authToken: null,
			refreshToken: null,
			loginDate: 0,
			authRefresher: null,
			user: null
		}
	}

	@MutationAction({ mutate: ['authToken'] })
	async setAuthToken(authToken){
		return { authToken }
	}
	@MutationAction({ mutate: ['user'] })
	async setUser(user){
		return { user }
	}
	@MutationAction({ mutate: ['user'] })
	async setUserName(name){
		return { user: { ...this.state.user, name } }
	}
	@MutationAction({ mutate: ['user'] })
	async setUserEmail(email){
		return { user: { ...this.state.user, email } }
	}
	@MutationAction({ mutate: ['user'] })
	async setUserRole(role){
		return { user: { ...this.state.user, role } }
	}
	get isSuperAdmin(){
		if (!this.user) return false;
		return this.user && this.user.role == TUserRole.SUPER_ADMIN;
	}
	get isLoggedIn(){
		return !!this.authToken;
	}
	get role(){
		if (!this.user) return null;
		return this.user.role;
	}
	get checkRole(){
		return (role) => this.authToken && this.user && (role in T_ROLE_DOUBLES || T_ROLE_DOUBLES.hasOwnProperty(role)) && T_ROLE_DOUBLES[role].includes(this.user.role);
	}


	@MutationAction({ mutate: ['authRefresher'] })
	async setAuthRefresher(authRefresher){
		if (this.state.authRefresher) {
			try{
				window.clearInterval(this.state.authRefresher);
			}catch(error){}
		}
		return { authRefresher }
	}

	get dateChanged(){
		return function(){
			return dateAsInt(new Date()) != this.loginDate;
		}
	}
}

const authStore = getModule(AuthStore);



export { name, AuthStore, authStore };
export default authStore;