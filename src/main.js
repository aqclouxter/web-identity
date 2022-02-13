import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from "./router";
import VueCrontab from 'vue-crontab'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrash, faLink, faCopy } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueEllipseProgress from 'vue-ellipse-progress';

Vue.use(VueEllipseProgress);
library.add(faTrash)
library.add(faLink)
library.add(faCopy)

Vue.component('font-awesome-icon', FontAwesomeIcon)



Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueCrontab)
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
