<script>
import VuePageTransition from 'vue-page-transition/src/components/VuePageTransition';

const MyPageTransition = {
	name: "MyPageTransition",
	extends: VuePageTransition,
	created(){
    	this.transition = this.$props.name;
	}
}
export { MyPageTransition }
export default MyPageTransition
</script>