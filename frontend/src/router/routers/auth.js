import { TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from "@/rpc/gen/auth_types";
import { RouterUser } from '@/router/user';

class AuthRouter extends RouterUser{
	constructor(stores=null, router=null){
		super(stores, router);
		console.log(router);
	}

	dialogRequireLogin(){
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda harus login terlebih dahulu",
			onDismiss: function(){ router.safePush({ name: "login"}) }
		});
		return false;
	}
	routeRequireLoginNow(to=null, from=null, next=null) {
		const router = this.router;
		if (!this.authStore.authToken){
			if (next) next(false);
			router.safePush({ name: "login" });
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
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda sudah login",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireLogoutNow(to=null, from=null, next=null) {
		const router = this.router;
		if (this.authStore.authToken){
			if (next) next(false);
			router.safePush({ name: "beranda" });
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
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Anda tidak memiliki hak untuk melakukan ini",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireRoleNow(to=null, from=null, next=null) {
		const router = this.router;
		if (!this.authStore.checkRole(role)){
			if (next) next(false);
			router.safePush({ path: "/" });
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
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Sesi kadaluarsa. Silahkan login ulang.",
			onDismiss: function(){ router.safePush({ name: "login"}) }
		});
		return false;
	}

	dialogIdleLogout() {
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Pemberitahuan",
			text: "Anda telah diam terlalu lama. Silahkan login kembali.",
			onDismiss: function(){ router.safePush({ path: "/login"}) }
		});
		return false;
	}

	dialogUnknownTAuthError(error, code){
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Sesi invalid (" + error + ":" + code + "). Silahkan login ulang atau laporkan bug.",
			onDismiss: function(){ router.safePush({ path: "/login"}) }
		});
		return false;
	}
	dialogUnknownError (error){
		const router = this.router;
		this.appStore.pushTabDialog({
			title: "Error",
			text: "Error tidak diketahui: " + error,
			onDismiss: function(){ window.location.reload() }
		});
		return false;
	}
}

const authRouter = new AuthRouter();

export { AuthRouter, authRouter }

export default authRouter;