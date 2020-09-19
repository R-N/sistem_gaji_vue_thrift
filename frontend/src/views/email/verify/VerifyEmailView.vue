<template>
	<center-layout column>
		<v-card>
			<change-email-form :token="token" v-if="hasPassword"/>
			<verify-email-form :token="token" v-else/>
		</v-card>
	</center-layout>
</template>
<script>
import { TLoginError, TLoginErrorCode, T_LOGIN_ERROR_STR } from '@/rpc/gen/user.auth.errors_types';
import { TUserError, TUserErrorCode, T_USER_ERROR_STR } from "@/rpc/gen/user.user.errors_types";
import { TEmailError, TEmailErrorCode, T_EMAIL_ERROR_STR } from '@/rpc/gen/user.email.errors_types';

import { authRouter } from '@/router/routers/auth';
import stores from "@/store/stores";
import { router } from '@/router/index';

import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import VerifyEmailForm from '@/views/email/verify/VerifyEmailForm';
import ChangeEmailForm from '@/views/email/verify/ChangeEmailForm';
import CenterLayout from '@/components/layout/CenterLayout';

@Component({
  	name: "VerifyEmailView",
  	//beforeRouteEnter: authRouter.routeRequireLogoutNow(),
	components: {
		CenterLayout,
		VerifyEmailForm,
		ChangeEmailForm
	}
})
class VerifyEmailView extends BaseView {
	hasPassword = true;

	get token(){
		return this.$route.params.token;
	}

	onInvalidToken(code){
		stores.app.pushTabDialog({
			title: "Error",
			text: T_EMAIL_ERROR_STR[code],
			onDismiss: function(){ router.safePush({ name: "beranda" }) }
		});
	}

	async mounted(){
		if (!this.token){
			this.onInvalidToken(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID);
			return;
		}
		this.busy = true;
		await this.checkHasPassword();
	}

	async checkHasPassword(){
		const view = this;
		view.busy = true;
		try{
			view.hasPassword = await stores.client.user.email.has_password(view.token);
		} catch (error) {
			if (error instanceof TEmailError){
				if (error.code == TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID
					|| error.code == TEmailErrorCode.EMAIL_TOKEN_INVALID){
					this.onInvalidToken(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID);
					return;
				}else if (error.code == TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED
					|| error.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED){
					this.onInvalidToken(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED);
					return;
				}
			}
			this.handleError(error);
		} finally {
			view.busy = false;
		}
	}

	handleError(error){
		if (error instanceof TLoginError){
			stores.app.pushTabDialog({
				title: "Error",
				text: T_LOGIN_ERROR_STR[error.code]
			});
		}else if (error instanceof TUserError){
			stores.app.pushTabDialog({
				title: "Error",
				text: T_USER_ERROR_STR[error.code]
			});
		}else if (error instanceof TEmailError){
			stores.app.pushTabDialog({
				title: "Error",
				text: T_EMAIL_ERROR_STR[error.code]
			});
		}else{
			throw error;
		}
	}

}
export { VerifyEmailView }
export default VerifyEmailView
</script>

<style scoped>

</style>
