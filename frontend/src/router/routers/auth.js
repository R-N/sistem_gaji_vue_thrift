import { TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode } from "@/rpc/gen/auth_types";
import { RouterUser } from '@/router/user';

class AuthRouter extends RouterUser{
	constructor(stores=null, router=null){
		super(stores, router);
		console.log(router);
	}

	dialogRequireLogin(){
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Error",
			text: "Anda harus login terlebih dahulu",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireLoginNow(){
		const obj = this;
		return function(to=null, from=null, next=null) {
			const router = obj.router;
			if (!obj.stores.auth.authToken){
				if (next) next(false);
				router.safePush({ name: "beranda" });
				return obj.dialogRequireLogin();
			}
			if (next) next();
			return true;
		}
	}
	routeRequireLoginDialog(){ 
		const obj = this;
		return function(to=null, from=null, next=null) {
			if (!obj.stores.auth.authToken){
				if (next) next(false);
				return obj.dialogRequireLogin();
			}
			if (next) next();
			return true;
		}
	}


	dialogRequireLogout(){
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Error",
			text: "Anda sudah login",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireLogoutNow(){
		const obj = this;
		return function(to=null, from=null, next=null) {
			const router = obj.router;
			if (obj.stores.auth.authToken){
				if (next) next(false);
				router.safePush({ name: "beranda" });
				return obj.dialogRequireLogout();
			}
			if (next) next();
			return true;
		}
	}
	routeRequireLogoutDialog(){
		const obj = this;
		return function(to=null, from=null, next=null) {
			if (obj.stores.auth.authToken){
				if (next) next(false);
				return obj.dialogRequireLogout();
			}
			if (next) next();
			return true;
		}
	}


	dialogRequireRole(){
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Error",
			text: "Anda tidak memiliki hak untuk melakukan ini",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	routeRequireRoleNow(role){
		const obj = this;
		return function(to=null, from=null, next=null) {
			const router = obj.router;
			if (!obj.stores.auth.checkRole(role)){
				if (next) next(false);
				router.safePush({ name: "beranda" });
				return obj.dialogRequireRole();
			}
			if (next) next();
			return true;
		}
	}
	routeRequireRoleDialog(role){
		const obj = this;
		return function(to=null, from=null, next=null) {
			if (!obj.stores.auth.checkRole(role)){
				if (next) next(false);
				return obj.dialogRequireRole();
			}
			if (next) next();
			return true;
		}
	}

	dialogSessionExpired(){
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Error",
			text: "Sesi kadaluarsa. Silahkan login ulang.",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}

	dialogIdleLogout() {
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Pemberitahuan",
			text: "Anda telah diam terlalu lama. Silahkan login kembali.",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}

	dialogUnknownTAuthError(error, code){
		const router = this.router;
		this.stores.app.pushTabDialog({
			title: "Error",
			text: "Sesi invalid (" + error + ":" + code + "). Silahkan login ulang atau laporkan bug.",
			onDismiss: function(){ router.safePush({ name: "beranda"}) }
		});
		return false;
	}
	dialogUnknownError (error){
		const router = this.router;
		this.stores.app.pushTabDialog({
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