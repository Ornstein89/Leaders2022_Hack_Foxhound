import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

let opts = {
  routes: [
    {
      path: "/",
      name: "FilesTable",
      component: () => import("../views/FilesTable.vue"),
    },
    {
      path: "/create",
      name: "UploadFile",
      component: () => import("../views/UploadFile.vue"),
    },
  ],
  linkExactActiveClass: "active",
};
const router = new VueRouter(opts);

export default router;
