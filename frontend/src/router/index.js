import Vue from "vue";
import VueRouter from "vue-router";
import { Auth } from "aws-amplify";

import Home from "../views/Home.vue";
import Transcript from "../views/Transcript.vue";
import Login from "../views/Login.vue";
import NewCourse from "../views/NewCourse.vue";
import Course from "../views/Course.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/transcript",
    name: "Transcript",
    component: Transcript,
    meta: { requiresAuth: true },
  },
  {
    path: "/new",
    name: "New Course",
    component: NewCourse,
    meta: { requiresAuth: true },
  },
  {
    path: "/course/:id",
    name: "Course",
    component: Course,
    meta: { requiresAuth: true },
  },
  {
    path: "/about",
    name: "About",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  routes,
});

router.beforeResolve((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    Auth.currentAuthenticatedUser()
      .then((res) => {
        // if the user is not set
        // if (!store.state.user) {
        //   // request the user and set it
        //   console.log(res);
        // }
        next();
      })
      .catch(() => {
        next({ path: "/login" });
      });
  }

  next();
});

export default router;
