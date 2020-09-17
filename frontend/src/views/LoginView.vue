<template>
	<center-layout column>
		<slide-x-left-transition
			:delay="transitionDelay"
			:duration="transitionDuration"
		>
			<div v-if="slide==0" :key="0">
				<v-card>
					<login-form/>
					<v-card-text class="pt-0">
						<div class="d-flex justify-end px-2 pb-2">
							<a href="#" @click.stop.prevent="slide = 1">Lupa password</a>
						</div>
						<div class="d-flex justify-end px-2 pb-2">
							<a href="#" @click.stop.prevent="slide = 2">Verifikasi email</a>
						</div>
					</v-card-text>
				</v-card>
			</div>
		</slide-x-left-transition>
		<slide-x-right-transition
			:delay="transitionDelay"
			:duration="transitionDuration"
		>
			<div v-if="slide==1" :key="1">
				<v-card>
					<forgot-password-form />
					<v-card-text class="pt-0">
						<div class="d-flex justify-start px-2 pb-2">
							<a href="#" @click.stop.prevent="slide = 0">Kembali</a>
						</div>
					</v-card-text>
				</v-card>
			</div>
		</slide-x-right-transition>
		<slide-x-right-transition
			:delay="transitionDelay"
			:duration="transitionDuration"
		>
			<div v-if="slide==2" :key="2">
				<v-card>
					<resend-verification-form />
					<v-card-text class="pt-0">
						<div class="d-flex justify-start px-2 pb-2">
							<a href="#" @click.stop.prevent="slide = 0">Kembali</a>
						</div>
					</v-card-text>
				</v-card>
			</div>
		</slide-x-right-transition>
	</center-layout>
</template>
<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import ImageBackground from '@/components/general/ImageBackground'
import LoginForm from '@/components/login/LoginForm'
import ForgotPasswordForm from '@/components/login/ForgotPasswordForm'
import ResendVerificationForm from '@/components/login/ResendVerificationForm'
import LoadingOverlay from '@/components/general/LoadingOverlay';
import CenterLayout from '@/components/general/CenterLayout';
import { SlideXLeftTransition, SlideXRightTransition } from 'vue2-transitions'

@Component({
  	name: "LoginView",
  	beforeRouteEnter: authRouter.routeRequireLogoutDialog,
	components: {
		ImageBackground,
		LoginForm,
		LoadingOverlay,
		CenterLayout,
		SlideXLeftTransition,
		SlideXRightTransition,
		ForgotPasswordForm,
		ResendVerificationForm
	}
})
class LoginView extends BaseView {
	@Prop({ default: 0 }) slide;

	transitionDuration = {
		enter: 300,
		leave: 300
	}
	transitionDelay = {
		enter: 300,
		leave: 0
	}
}
export { LoginView }
export default LoginView
</script>

<style scoped>

</style>
