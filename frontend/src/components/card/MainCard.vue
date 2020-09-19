<template>
	<v-row
		align="start"
		justify="start"
	>
		<v-col
			align="start"
			justify="start"
		>
			<v-card class="fill-width py-2 px-4">
				<card-title :title="title" />
				<card-toolbar v-if="!noToolbar">
					<template v-slot:left>
						<slot name="toolbar-left"></slot>
    				</template>
    				<template v-slot:right>
						<slot name="toolbar-right"></slot>
    				</template>
				</card-toolbar>
				<v-card-text>
					<slot name="content"></slot>
					<slot name="default"></slot>
				</v-card-text>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

import CardTitle from '@/components/card/CardTitle';
import CardToolbar from '@/components/card/CardToolbar';

@Component({
  	name: "MainCard",
  	components: {
  		CardTitle,
  		CardToolbar
  	}
})
class MainCard extends Vue {
	@Prop({ default: "Title" }) title;
	@Prop({ default: false }) noToolbar;
}
export { MainCard } 
export default MainCard
</script>
<style scoped>
</style>
