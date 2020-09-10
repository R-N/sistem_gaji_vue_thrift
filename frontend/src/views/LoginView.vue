<template>
	<v-container
		class="fill-height"
		fluid
	>
		<v-row
			align="center"
			justify="center"
		>
			<login-form/>
		</v-row>
	</v-container>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { authRouter } from '@/router/routers/auth';
import ImageBackground from '@/components/ImageBackground'
import LoginForm from '@/components/LoginForm'
import LoadingOverlay from '@/components/LoadingOverlay';

@Component({
  	name: "LoginView",
  	beforeRouteEnter: authRouter.routeRequireLogoutDialog,
	components: {
		ImageBackground,
		LoginForm,
		LoadingOverlay
	}
})
class LoginView extends BaseView {
}
export { LoginView }
export default LoginView
</script>

<style scoped>

</style>
