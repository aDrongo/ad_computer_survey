import Vue from 'vue'
import App from './App'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.config.productionTip = false

axios.defaults.baseURL = 'http://localhost:5000'

new Vue({
  render: h => h(App),
}).$mount('#app')
