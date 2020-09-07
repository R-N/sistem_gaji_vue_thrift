<template>
    <v-main>
		<v-container
			class="fill-height"
			fluid
		>
			<v-row
				align="center"
				justify="center"
				class="flex-column"
			>
				<h1>Server is down</h1>
				<refresh-button icon large/>
			</v-row>
		</v-container>
    </v-main>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';
import RefreshButton from '@/components/RefreshButton';

@Component({
  	name: "ServerDownView",
  	components: {
  		RefreshButton
  	}
})
class ServerDownView extends BaseView {

}
export { ServerDownView } ;
export default ServerDownView;
</script>

<style scoped>

</style>
