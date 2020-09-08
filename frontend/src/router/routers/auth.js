import { AuthError, AuthErrorCode, LoginError, LoginErrorCode } from "@/rpc/gen/auth_types";
import { RouterUser } from '@/router/user';

class AuthRouter extends RouterUser{
	constructor(stores=null, router=null){
		super(stores, router);
	}

	dialogRequireLogin(){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda harus login terlebih dahulu",
			onDismiss: function(){ this.router.safePush({ name: "login"}) }
		});
		return false;
	}
	routeRequireLoginNow(to=null, from=null, next=null) {
		if (!this.authStore.authToken){
			if (next) next(false);
			this.router.safePush({ name: "login" });
			return false;
		}
		if (next) next();
		return true;
	}
	routeRequireLoginDialog (to=null, from=null, next=null) {
		if (!this.authStore.authToken){
			if (next) next(false);
			return dialogRequireLogin();
		}
		if (next) next();
		return true;
	}


	dialogRequireLogout(){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda sudah login",
			onDismiss: function(){ this.router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireLogoutNow(to=null, from=null, next=null) {
		if (this.authStore.authToken){
			if (next) next(false);
			this.router.safePush({ name: "beranda" });
			return false;
		}
		if (next) next();
		return true;
	}
	routeRequireLogoutDialog (to=null, from=null, next=null) {
		if (this.authStore.authToken){
			if (next) next(false);
			return dialogRequireLogout();
		}
		if (next) next();
		return true;
	}


	dialogRequireRole(){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda tidak memiliki hak untuk melakukan ini",
			onDismiss: function(){ this.router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireRoleNow(to=null, from=null, next=null) {
		if (!this.authStore.checkRole(role)){
			if (next) next(false);
			this.router.safePush({ path: "/" });
			return false;
		}
		if (next) next();
		return true;
	}
	routeRequireRoleDialog(to=null, from=null, next=null) {
		if (!this.authStore.checkRole(role)){
			if (next) next(false);
			return dialogRequireRole();
		}
		if (next) next();
		return true;
	}

	dialogSessionExpired(){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Sesi kadaluarsa. Silahkan login ulang.",
			onDismiss: function(){ this.router.safePush({ name: "login"}) }
		});
		return false;
	}

	dialogIdleLogout() {
		this.appStore.pushTabDialog({
			title: "Pemberitahuan",
			text: "Anda telah diam terlalu lama. Silahkan login kembali.",
			onDismiss: function(){ this.router.safePush({ path: "/login"}) }
		});
		return false;
	}

	dialogUnknownAuthError(error, code){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Sesi invalid (" + error + ":" + code + "). Silahkan login ulang atau laporkan bug.",
			onDismiss: function(){ this.router.safePush({ path: "/login"}) }
		});
		return false;
	}
	dialogUnknownError (error){
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Error tidak diketahui: " + error,
			onDismiss: function(){ this.router.safePush({ path: "/login"}) }
		});
		return false;
	}
}

const authRouter = new AuthRouter();

export { AuthRouter, authRouter }

export default authRouter;