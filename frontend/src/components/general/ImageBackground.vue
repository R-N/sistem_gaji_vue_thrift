<template>
	<img class="bg" v-lazy="src"/>
</template>

<script>
import { Vue, Component, Prop } from 'vue-property-decorator';

@Component({
	name: "ImageBackground"
})
class ImageBackground extends Vue {
	@Prop(String) src
}
export { ImageBackground }
export default ImageBackground
</script>
<style scoped>
.bg {
	background-size: cover;
	opacity: 0.5;
	position: fixed;
	width: 100vw;
	height: 100vh;
	object-fit: cover;
}
</style>