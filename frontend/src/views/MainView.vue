<template>
	<my-page-transition appear name="overlay-down" class="fill-height" >
		<login-view appear v-if="!isLoggedIn" key="b"/>
		<v-container 
			appear
			class="" 
			align="start"
			justify="start"
			key="c"
			v-else
		>
	        <transition appear name="fade" mode="out-in">
				<v-row appear class="" align="start" justify="start"  v-if="serverReachable && isLoggedIn && breadcrumbs && breadcrumbs.length">
					<v-col align="start" justify="start">
					    <v-alert
							color="grey"
							text
					    >
				        	<v-breadcrumbs class="py-0" :items="breadcrumbs" large>
								<template v-slot:divider>
									<v-icon>mdi-chevron-right</v-icon>
								</template>
				        	</v-breadcrumbs>
					    </v-alert>
			        </v-col>
			    </v-row>
			</transition>
			<slide-y-down-transition 
				group
				appear
				:duration="transitionDuration"
				:delay="transitionDelay"
			>
				<router-view appear :key="$route.matched[1].path"/>
			</slide-y-down-transition>
  			<v-spacer></v-spacer>
		</v-container>
	</my-page-transition>
</template>

<script>
import { authStore, appStore, clientStore } from "@/store/stores";
import { router } from '@/router/index';

import { Component } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';

import { FadeTransition, SlideYDownTransition, SlideXLeftTransition, CollapseTransition } from 'vue2-transitions'
import LoginView from '@/views/general/login/LoginView';
import MyPageTransition from '@/components/general/MyPageTransition';

@Component({
	name: "MainView",
	components: {
		LoginView,
		SlideYDownTransition,
		SlideXLeftTransition,
		CollapseTransition,
		MyPageTransition
	}
})
class MainView extends BaseView{
	transitionDuration = {
		enter: 300,
		leave: 300
	}
	transitionDelay = {
		enter: 300,
		leave: 0
	}

	mounted(){
		console.log(this.$route);
	}
	get breadcrumbs(){
		return appStore.breadcrumbs;
	}


	get isLoggedIn(){
		return authStore.isLoggedIn;
	}
	get serverReachable(){
		return appStore.serverReachable;
	}
}
export { MainView }
export default MainView
</script>
