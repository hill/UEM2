import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Buefy from 'buefy'

// import * as Sentry from "@sentry/vue";
// import { Integrations } from "@sentry/tracing";


import API from './services/api.service'

// Sentry.init({
//   Vue: Vue,
//   dsn: "https://9fabfac1a4874239a0c878f65e2d1adc@o454372.ingest.sentry.io/5727387",
//   integrations: [new Integrations.BrowserTracing()],
//   tracesSampleRate: 1.0,
// });

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]
Vue.use(Buefy)

API.init();

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
