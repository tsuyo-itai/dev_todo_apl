import { createRouter, createWebHistory } from "vue-router";
import AuthView from "../views/AuthView.vue";
import AuthCreateView from "../views/AuthCreateView.vue";
import MuToDoListView from "../views/MyToDoListView.vue";

const routes = [
  {
    path: "/:catchAll(.*)",
    redirect: "/auth",
  },
  {
    path: "/auth",
    name: "auth",
    component: AuthView,
  },
  {
    path: "/auth/create",
    name: "authcreate",
    component: AuthCreateView,
  },
  {
    path: "/todos",
    name: "todos",
    component: MuToDoListView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
