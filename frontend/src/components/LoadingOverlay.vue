<template>
    <v-overlay :value="busy">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
</template>

<script>
import { Component, Prop } from 'vue-property-decorator';
import { WorkingComponent } from '@/components/WorkingComponent';

@Component({
	name: "LoadingOverlay"
})
class LoadingOverlay extends WorkingComponent {
	@Prop(String) src
}
export { LoadingOverlay }
export default LoadingOverlay
</script>
<style scoped>
</style>