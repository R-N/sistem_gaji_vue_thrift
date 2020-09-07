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

const requireLogin = (async=true) => (target, name, descriptor) => {
	const func = descriptor.value;
	if(async){
		descriptor.value = async function(...args) {
			if (!authStore.authToken) throw new AuthError({ code: AuthErrorCode.NOT_LOGGED_IN });
			return await func.apply(this, args);
		}
	}else{
		descriptor.value = function(...args) {
			if (!authStore.authToken) throw new AuthError({ code: AuthErrorCode.NOT_LOGGED_IN });
			return func.apply(this, args);
		}
	}
	return descriptor;
}
const requireLogout = (async=true) => (target, name, descriptor) => {
	const func = descriptor.value;
	if(async){
		descriptor.value = async function(...args) {
			if (authStore.authToken) throw new LoginError({ code: LoginErrorCode.ALREADY_LOGGED_IN });
			return await func.apply(this, args);
		}
	}else{
		descriptor.value = function(...args) {
			if (authStore.authToken) throw new LoginError({ code: LoginErrorCode.ALREADY_LOGGED_IN });
			return func.apply(this, args);
		}
	}
	return descriptor;
}
const requireRole = (role, async=true) => (target, name, descriptor) => {
	const func = descriptor.value;
	if (async){
		descriptor.value = async function(...args) {
			if (!authStore.checkRole(role)) throw new AuthError({ code: AuthErrorCode.INVALID_ROLE });
			return await func.apply(this, arguments);
		}
	}else{
		descriptor.value = function(...args) {
			if (!authStore.checkRole(role)) throw new AuthError({ code: AuthErrorCode.INVALID_ROLE });
			return func.apply(this, arguments);
		}
	}
	return descriptor;
}


export { name, AuthStore, authStore, requireLogin, requireRole, requireLogout };
export default authStore;