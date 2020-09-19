<template>
	<v-card-title class="my-0 pb-0" align="start">
		<v-row>
			<v-col align="start" justify="start">
				<slot name="left"></slot>
			</v-col>
			<v-spacer></v-spacer>
			<v-col align="start" justify="start">
				<slot name="right"></slot>
			</v-col>
		</v-row>
	</v-card-title>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
  	name: "CardToolbar"
})
class CardToolbar extends Vue {
}
export { CardToolbar } 
export default CardToolbar
</script>
<style scoped>
</style>
