<template>
	<v-card-title class="my-0 pb-0" align="start">
		<v-row>
			<v-col align="start" justify="start">
				<slot>
					<h2 class="text-h2">{{ title }}</h2>
				</slot>
			</v-col>
		</v-row>
	</v-card-title>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
  	name: "CardTitle"
})
class CardTitle extends Vue {
	@Prop({ default: "Title" }) title;
}
export { CardTitle } 
export default CardTitle
</script>
<style scoped>
</style>
