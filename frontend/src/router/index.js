import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

let opts = {
  routes: [
    {
      path: "/",
      name: "Index",
      component: () => import("../views/Index.vue"),
      meta: {
        requiresAuth: false,
      },
    },
  ],
  linkExactActiveClass: "active",
};
const router = new VueRouter(opts);

export default router;
