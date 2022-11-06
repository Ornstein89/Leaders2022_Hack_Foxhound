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
    {
      path: "/viewlabeling/:id",
      name: "ViewLabeling",
      component: () => import("../views/ViewLabeling.vue"),
      props: true,
    },
    {
      path: "/viewgenerate/:id/setup",
      name: "ViewGenerationSetup",
      component: () => import("../views/ViewGeneration.vue"),
      props: true,
    },
    {
      path: "/viewgenerate/:id",
      name: "ViewGeneration",
      component: () => import("../views/ViewGeneration.vue"),
      props: true,
    },
    // {
    //   path: "/viewlabeling2/:id",
    //   name: "ViewLabeling_dwvjqui",
    //   component: () => import("../views/ViewLabeling_dwvjqui.vue"),
    //   props: true,
    // },
  ],
  linkExactActiveClass: "active",
};
const router = new VueRouter(opts);

export default router;
