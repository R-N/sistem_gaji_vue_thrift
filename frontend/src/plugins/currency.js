import Vue from 'vue'
import VCurrencyField from 'v-currency-field'
import { VTextField } from 'vuetify/lib'  //Globally import VTextField

Vue.component('v-text-field', VTextField)

const params = { 
	locale: 'id-ID',
	decimalLength: 0,
	autoDecimalMode: true,
	min: 0,
	max: null,
	defaultValue: 0,
    valueAsInteger: false,
    allowNegative: false
}

const init = (Vue) => Vue.use(VCurrencyField, params);

export { VCurrencyField, params, init}
export default init;
