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
    {
      path: "/viewlabeling/:id",
      name: "ViewLabeling",
      component: () => import("../views/ViewLabeling.vue"),
      meta: {
        requiresAuth: false,
      },
      props : true,
    },
  ],
  linkExactActiveClass: "active",
};
const router = new VueRouter(opts);

export default router;
