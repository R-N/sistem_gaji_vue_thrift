<template>
	<v-container
		class="fill-height flex-grow-1"
		fluid
	>
		<v-row
			align="center"
			justify="center"
			:class="myClass"
		>
			<slot></slot>
		</v-row>
	</v-container>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
  	name: "CenterLayout",
})
class CenterLayout extends Vue {
	@Prop({ default: false }) column;

	get myClass(){
		if(this.column)
			return "flex-column"
		else
			return ""
	}
}
export { CenterLayout }
export default CenterLayout
</script>

<style scoped>

</style>
