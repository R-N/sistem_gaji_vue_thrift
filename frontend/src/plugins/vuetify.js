import Vue from 'vue';
import Vuetify from 'vuetify/lib';
//import { VNumberInput } from 'vuetify/labs/VNumberInput';
//import { createVuetify } from 'vuetify'

Vue.use(Vuetify);

export default new Vuetify({
	// components: {
	//   VNumberInput,
	// },
	theme: {
		themes: {
			light: {
				primary: '#303382'
			},
		},
	},
});
