import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Axios from "axios";
import store from "./store";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;
new Vue({
  router,
  store: store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
Axios.defaults.headers.common["Content-Type"] = "application/json";
