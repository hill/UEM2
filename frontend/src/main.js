import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import API from './services/api.service'

Vue.config.productionTip = false
API.init();

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
