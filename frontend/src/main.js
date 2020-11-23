import Vue from 'vue'
import App from './App'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.config.productionTip = false

//switch if not using a reverse proxy.
//axios.defaults.baseURL = window.location.origin.split(':')[0] + ':' + window.location.origin.split(':')[1] + ":5000/api"
axios.defaults.baseURL = window.location.origin + "/api"

new Vue({
  render: h => h(App),
}).$mount('#app')
