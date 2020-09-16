<template>
	<vue-page-transition name="overlay-down" class="fill-height">
		<login-view v-if="!isLoggedIn" key="b"/>
		<v-container 
			class="" 
			align="start"
			justify="start"
			key="c"
			v-else
		>
	        <transition name="fade" mode="out-in">
				<v-row class="" align="start" justify="start"  v-if="serverReachable && isLoggedIn && breadcrumbs && breadcrumbs.length">
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
				<slide-y-down-transition group>
					<router-view appear :key="$route.matched[1].path"/>
				</slide-y-down-transition>
  			<v-spacer></v-spacer>
		</v-container>
	</vue-page-transition>
</template>

<script>

import { authStore, appStore, clientStore } from "@/store/stores";
import { Component } from 'vue-property-decorator'
import { BaseView } from '@/views/BaseView';
import LoginView from '@/views/LoginView';
import { router } from '@/router/index';
import {SlideYDownTransition, CollapseTransition} from 'vue2-transitions'

@Component({
	name: "MainView",
	components: {
		LoginView,
		SlideYDownTransition,
		CollapseTransition
	}
})
class MainView extends BaseView{

	drawer = false;
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
