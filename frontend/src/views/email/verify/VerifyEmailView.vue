<template>
	<center-layout column>
		<v-card>
			<change-email-form :token="token" v-if="hasPassword"/>
			<verify-email-form :token="token" v-else/>
		</v-card>
	</center-layout>
</template>
<script>
import { TLoginError } from '@/rpc/gen/user.auth.errors_types';
import { TUserError } from "@/rpc/gen/user.user.errors_types";
import { TUserEmailError, T_USER_EMAIL_ERROR_STR } from '@/rpc/gen/user.email.errors_types';
import { TEmailError } from '@/rpc/gen/email.errors_types';

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
			stores.helper.error.showError(
				T_USER_EMAIL_ERROR_STR[TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID], 
				"beranda"
			);
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
					stores.helper.error.showError(
						T_EMAIL_ERROR_CODE_STR[TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID]
					);
					return;
				}else if (error.code == TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED
					|| error.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED){
					stores.helper.error.showError(
						T_EMAIL_ERROR_CODE_STR[TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED]
					);
					return;
				}
			}
			if (stores.helper.error.showFilteredError(error, 
				[TLoginError, TUserError, TEmailError, TUserEmailError]
			)) return;
			throw error;
		} finally {
			view.busy = false;
		}
	}


}
export { VerifyEmailView }
export default VerifyEmailView
</script>

<style scoped>

</style>
