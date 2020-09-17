<template>
	<center-layout>
		<h1>404 Not Found: {{ this.$route.params.pathMatch }}</h1>
	</center-layout>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import stores from '@/store/stores';
import CenterLayout from '@/components/general/CenterLayout';

@Component({
  	name: "NotFoundView",
  	components:{
  		CenterLayout
  	},
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
