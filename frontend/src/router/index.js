import Vue from "vue";
import VueRouter from "vue-router";
import API from '../services/api.service';

import Home from "../views/Home.vue";
import Transcript from "../views/Transcript.vue";
import Login from "../views/Login.vue";
import NewCourse from "../views/NewCourse.vue";
import Course from "../views/Course.vue";
import jwtService from "../services/jwt.service";

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
  const token = jwtService.getToken();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (!requiresAuth) next();
  if (!token) {console.log('no token!'); next('/login') } else {API.setHeader();}
  // redirect if going to login, already logged in
  if (to.path === '/login') {
		if (token) {
			API.post('/auth/verify').then(() => {
				next('/transcript');
			}).catch(() => {
				next();
			});
		} else {
			next();
		}
	}
  if (requiresAuth && token) {
    // verify the token is valid
    API.post('/auth/verify').then(() => {
      next();
    }).catch(() => {
      console.log("TOKEN INVALID!")
      next('/login');
    });
  }
});

export default router;
