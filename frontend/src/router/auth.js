import { router } from '@/router/index';
import { authStore, appStore } from '@/store/stores';
import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";

const dialogRequireLogin = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda harus login terlebih dahulu",
		onDismiss: function(){ router.push({ path: "/login"}) }
	});
	return false;
}
const routeRequireLogin = (immediate=false) =>{
	if (immediate){
		return async function(to=null, from=null, next=null) {
			if (!authStore.authToken){
				if (next) next(false);
				await router.push({ name: "login" });
				return false;
			}
			if (next) next();
			return true;
		}
	} else {
		return function(to=null, from=null, next=null) {
			if (!authStore.authToken){
				if (next) next(false);
				return dialogRequireLogin();
			}
			if (next) next();
			return true;
		}
	}
}
const dialogRequireLogout = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda sudah login",
		onDismiss: function(){ router.push({ name: "beranda"}) }
	});
	return false;
}
const routeRequireLogout = (immediate=false) =>{
	if (immediate){
		return async function(to=null, from=null, next=null) {
			if (authStore.authToken){
				if (next) next(false);
				await router.push({ name: "beranda" });
				return false;
			}
			if (next) next();
			return true;
		}
	} else {
		return function(to=null, from=null, next=null) {
			if (authStore.authToken){
				if (next) next(false);
				return dialogRequireLogout();
			}
			if (next) next();
			return true;
		}
	}
}
const dialogRequireRole = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda tidak memiliki hak untuk melakukan ini",
		onDismiss: function(){ router.push({ path: "/"}) }
	});
	return false;
}
const routeRequireRole = (role, immediate=false) =>{
	if (immediate){
		return async function(to=null, from=null, next=null) {
			if (!authStore.checkRole(role)){
				if (next) next(false);
				await router.push({ path: "/" });
				return false;
			}
			if (next) next();
			return true;
		}
	} else {
		return function(to=null, from=null, next=null) {
			if (!authStore.checkRole(role)){
				if (next) next(false);
				return dialogRequireRole();
			}
			if (next) next();
			return true;
		}
	}
}

export { routeRequireLogin, routeRequireLogout, routeRequireRole, dialogRequireLogin, dialogRequireLogout, dialogRequireRole }
export default { routeRequireLogin, routeRequireLogout, routeRequireRole }