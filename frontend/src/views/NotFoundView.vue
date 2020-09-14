<template>
	<v-container
		class="fill-height"
		fluid
	>
		<v-row
			align="center"
			justify="center"
		>
			<h1>404 Not Found: {{ this.$route.params.pathMatch }}</h1>
		</v-row>
	</v-container>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import stores from '@/store/stores';

@Component({
  	name: "NotFoundView",
	beforeRouteLeave: function (to, from, next) {
		stores.app.setRouteValid(true);
		next();
	},
	beforeRouteEnter: function (to, from, next) {
		stores.app.setRouteValid(false);
		next();
	}
})
class NotFoundView extends BaseView {

}
export { NotFoundView } ;
export default NotFoundView;
</script>

<style scoped>

</style>
