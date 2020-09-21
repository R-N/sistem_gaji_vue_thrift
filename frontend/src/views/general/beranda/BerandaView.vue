<template>
	<center-layout >
		<h1>Ini beranda</h1>
	</center-layout>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { BaseView } from '@/views/BaseView';

import CenterLayout from '@/components/layout/CenterLayout';

@Component({
  	name: "BerandaView",
  	components: {
  		CenterLayout
  	}
})
class BerandaView extends BaseView {
}
export { BerandaView } ;
export default BerandaView;
</script>

<style scoped>

</style>
