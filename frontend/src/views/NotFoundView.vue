<template>
    <v-main>
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
    </v-main>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

@Component({
  	name: "NotFoundView"
})
class NotFoundView extends BaseView {

}
export { NotFoundView } ;
export default NotFoundView;
</script>

<style scoped>

</style>
