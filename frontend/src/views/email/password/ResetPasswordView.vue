<template>
	<center-layout column>
		<v-card>
			<reset-password-form :token="token" />
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

import ResetPasswordForm from '@/views/email/password/ResetPasswordForm';
import CenterLayout from '@/components/layout/CenterLayout';

@Component({
  	name: "VerifyEmailView",
  	//beforeRouteEnter: authRouter.routeRequireLogoutNow(),
	components: {
		CenterLayout,
		ResetPasswordForm
	}
})
class VerifyEmailView extends BaseView {

	get token(){
		return this.$route.params.token;
	}

	onError(message){
		stores.app.pushTabDialog({
			title: "Error",
			text: message,
			onDismiss: function(){ router.safePush({ name: "beranda" }) }
		});
	}

	async mounted(){
		if (!this.token){
			this.onInvalidToken(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID);
			return;
		}
	}


	handleError(error){
		if (error instanceof TLoginError){
			this.onError(T_LOGIN_ERROR_STR[error.code]);
		}else if (error instanceof TUserError){
			this.onError(T_USER_ERROR_STR[error.code]);
		}else if (error instanceof TEmailError){
			this.onError(T_EMAIL_ERROR_STR[error.code]);
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
