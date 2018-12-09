// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'core-js/es6/promise'
import 'core-js/es6/string'
import 'core-js/es7/array'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCurrencyFilter from 'vue-currency-filter'
import LoadScript from 'vue-plugin-load-script';
import VueCookies from 'vue-cookies'


// Global modules
Vue.use(LoadScript);
Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.use(VueCookies)
Vue.use(VueCurrencyFilter,
  {
    symbol : '€',
    thousandsSeparator: ',',
    fractionCount: 2,
    fractionSeparator: '.',
    symbolPosition: 'front',
    symbolSpacing: true
  })
  

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})
