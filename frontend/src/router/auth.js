import { router } from '@/router/index';
import { authStore, appStore } from '@/store/stores';
import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";

const dialogRequireLogin = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda harus login terlebih dahulu",
		onDismiss: function(){ router.push({ name: "login"}) }
	});
	return false;
}
const routeRequireLoginNow = function(to=null, from=null, next=null) {
	if (!authStore.authToken){
		if (next) next(false);
		router.push({ name: "login" });
		return false;
	}
	if (next) next();
	return true;
}
const routeRequireLoginDialog = function(to=null, from=null, next=null) {
	if (!authStore.authToken){
		if (next) next(false);
		return dialogRequireLogin();
	}
	if (next) next();
	return true;
}


const dialogRequireLogout = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda sudah login",
		onDismiss: function(){ router.push({ name: "beranda"}) }
	});
	return false;
}
const routeRequireLogoutNow = function(to=null, from=null, next=null) {
	if (authStore.authToken){
		if (next) next(false);
		router.push({ name: "beranda" });
		return false;
	}
	if (next) next();
	return true;
}
const routeRequireLogoutDialog = function(to=null, from=null, next=null) {
	if (authStore.authToken){
		if (next) next(false);
		return dialogRequireLogout();
	}
	if (next) next();
	return true;
}


const dialogRequireRole = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda tidak memiliki hak untuk melakukan ini",
		onDismiss: function(){ router.push({ name: "beranda"}) }
	});
	return false;
}
const routeRequireRoleNow = function(to=null, from=null, next=null) {
	if (!authStore.checkRole(role)){
		if (next) next(false);
		router.push({ path: "/" });
		return false;
	}
	if (next) next();
	return true;
}
const routeRequireRoleDialog = function(to=null, from=null, next=null) {
	if (!authStore.checkRole(role)){
		if (next) next(false);
		return dialogRequireRole();
	}
	if (next) next();
	return true;
}

const dialogSessionExpired = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Sesi kadaluarsa. Silahkan login ulang.",
		onDismiss: function(){ router.push({ name: "login"}) }
	});
	return false;
}

export { 
	routeRequireLoginNow, 
	routeRequireLogoutNow, 
	routeRequireRoleNow, 
	routeRequireLoginDialog, 
	routeRequireLogoutDialog, 
	routeRequireRoleDialog,
	dialogRequireLogin, 
	dialogRequireLogout, 
	dialogRequireRole,
	dialogSessionExpired
}

export default { 
	routeRequireLoginNow, 
	routeRequireLogoutNow, 
	routeRequireRoleNow, 
	routeRequireLoginDialog, 
	routeRequireLogoutDialog, 
	routeRequireRoleDialog,
	dialogRequireLogin, 
	dialogRequireLogout, 
	dialogRequireRole,
	dialogSessionExpired
}