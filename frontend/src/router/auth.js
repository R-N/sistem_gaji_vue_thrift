import { router } from '@/router/index';
import { authStore } from '@/store/modules/auth';
import { appStore } from '@/store/modules/app';
import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";

const dialogRequireLogin = () => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Anda harus login terlebih dahulu",
		onDismiss: function(){ router.safePush({ name: "login"}) }
	});
	return false;
}
const routeRequireLoginNow = function(to=null, from=null, next=null) {
	if (!authStore.authToken){
		if (next) next(false);
		router.safePush({ name: "login" });
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
		onDismiss: function(){ router.safePush({ name: "beranda"}) }
	});
	return false;
}
const routeRequireLogoutNow = function(to=null, from=null, next=null) {
	if (authStore.authToken){
		if (next) next(false);
		router.safePush({ name: "beranda" });
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
		onDismiss: function(){ router.safePush({ name: "beranda"}) }
	});
	return false;
}
const routeRequireRoleNow = function(to=null, from=null, next=null) {
	if (!authStore.checkRole(role)){
		if (next) next(false);
		router.safePush({ path: "/" });
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
		onDismiss: function(){ router.safePush({ name: "login"}) }
	});
	return false;
}

const dialogIdleLogout = () => {
	appStore.pushTabDialog({
		title: "Pemberitahuan",
		text: "Anda telah diam terlalu lama. Silahkan login kembali.",
		onDismiss: function(){ router.safePush({ path: "/login"}) }
	});
	return false;
}

const dialogUnknownAuthError = (error, code) => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Sesi invalid (" + error + ":" + code + "). Silahkan login ulang atau laporkan bug.",
		onDismiss: function(){ router.safePush({ path: "/login"}) }
	});
	return false;
}
const dialogUnknownError = (error) => {
	appStore.pushTabDialog({
		title: "Error",
		text: "Error tidak diketahui: " + error,
		onDismiss: function(){ router.safePush({ path: "/login"}) }
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
	dialogSessionExpired,
	dialogIdleLogout,
	dialogUnknownAuthError
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
	dialogSessionExpired,
	dialogIdleLogout,
	dialogUnknownAuthError
}