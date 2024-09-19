// import VueJustSuper from "vue-just-super";
// import VueSuper from 'vue-super';
import VueSuperMethod from 'vue-super-call';

//const init = (Vue) => Vue.use(VueJustSuper);
//const init = (Vue) => Vue.use(VueSuper);
const init = (Vue) => Vue.prototype.$super = VueSuperMethod;

export { init}
export default init;
