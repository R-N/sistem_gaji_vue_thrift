<template>
	<center-layout column="true">
		<h1>Server is down</h1>
		<refresh-button icon large/>
	</center-layout>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import CenterLayout from '@/components/layout/CenterLayout';
import RefreshButton from '@/components/general/RefreshButton';

@Component({
  	name: "ServerDownView",
  	components: {
  		RefreshButton,
  		CenterLayout
  	}
})
class ServerDownView extends BaseView {
}
export { ServerDownView } ;
export default ServerDownView;
</script>

<style scoped>

</style>
