<template>
    <v-main v-if="!isLoggedIn">
		<image-background :src="require('@/assets/img/login-background.png')"></image-background>
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
    </v-main>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import { routeRequireLogoutDialog } from '@/router/auth';
import ImageBackground from '@/components/ImageBackground'
import LoginForm from '@/components/LoginForm'
import LoadingOverlay from '@/components/LoadingOverlay';

@Component({
  	name: "LoginView",
  	//beforeRouteEnter: routeRequireLogoutDialog,
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
