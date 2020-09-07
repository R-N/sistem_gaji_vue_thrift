import {
	Action,
	Mutation,
	MutationAction,
	VuexModule,
	getModule,
	Module
} from "vuex-module-decorators";
import { store, unregisterModule } from "@/store/index";
import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";

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

	@MutationAction({ mutate: ['authToken', 'refreshToken'] })
	async setTokens(loginResult){
		var refreshToken = loginResult.refresh_token || this.state.refreshToken
		return {
			authToken: loginResult.auth_token,
			refreshToken
		};
	}

	@MutationAction({ mutate: ['authToken', 'refreshToken', 'authRefresher', 'user'] })
	async logout(){
		if (this.state.authRefresher) {
			try{
				window.clearInterval(this.state.authRefresher);
			}catch(error){}
		}
		return {
			authToken: null,
			refreshToken: null,
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
	get isLoggedIn(){
		return !!this.authToken;
	}
	get role(){
		if (!this.user) return null;
		return this.user.role;
	}
	get checkRole(){
		return (role) => this.authToken && this.user && (this.user.role === role);
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
}

const authStore = getModule(AuthStore);



export { name, AuthStore, authStore };
export default authStore;