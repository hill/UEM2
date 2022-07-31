import { createRouter, createWebHistory } from "vue-router";
import API from "../services/api.service";
import { AuthService } from "../services/api.service";
import jwtService from "../services/jwt.service";
import { store } from "../store";

import Login from "../views/Login.vue";
import Transcript from "../views/Transcript.vue";
import Resources from "../views/Resources.vue";
import New from "../views/New.vue";
import Course from "../views/Course.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    redirect: "/resources",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/resources",
    name: "Resources",
    component: Resources,
    meta: { requiresAuth: false },
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
    component: New,
    meta: { requiresAuth: true },
  },
  {
    path: "/course/:id",
    name: "Course",
    component: Course,
    meta: { requiresAuth: true },
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeResolve(async (to, from, next) => {
  const token = jwtService.getToken();
  if (token) {
    API.setHeader();
  }
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  let loggedIn = false;

  try {
    const { data } = await AuthService.verify();
    if (data) {
      store.commit("setUser", data);
      loggedIn = true;
    }
  } catch (err) {
    if (requiresAuth) {
      next("/login");
    } else {
      next();
    }
  }

  // redirect if going to login, already logged in
  if (to.path === "/login") {
    if (token && loggedIn) {
      next("/resources");
      return;
    }
  }

  if (token) {
    // Token refresh
    const expiry = JSON.parse(window.atob(token.split(".")[1]))["exp"] * 1000;
    const expiresIn = expiry - new Date().getTime();
    if (expiresIn < 2 * 60 * 1000 && expiresIn > 0) {
      // request a new token when it is < 2 minutes away from expiring
      try {
        const { data } = await AuthService.refresh();
        jwtService.saveToken(data.access);
        API.setHeader();
        next();
      } catch (err) {
        next("/login");
      }
    }
  }

  if (!requiresAuth) {
    next();
  } else if (requiresAuth && loggedIn) {
    next();
  } else {
    // you don't have a token!
    next("/login");
  }
});

export default router;
