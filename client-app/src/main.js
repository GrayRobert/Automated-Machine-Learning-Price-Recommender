// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'core-js/es6/promise'
import 'core-js/es6/string'
import 'core-js/es7/array'
// import cssVars from 'css-vars-ponyfill'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import VueD3 from 'vue2-d3'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCurrencyFilter from 'vue-currency-filter'


// todo
// cssVars()

Vue.use(BootstrapVue)
Vue.use(VueD3)
Vue.use(VueAxios, axios)

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
