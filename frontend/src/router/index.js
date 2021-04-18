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

  // Token refresh
  const expiry = JSON.parse(window.atob(token.split('.')[1]))["exp"] * 1000;
  const expiresIn = expiry - new Date().getTime()
  if (expiresIn < 100000 && expiresIn > 0) {
    // request a new token
    API.post('/auth/refresh').then(({data}) => {
      jwtService.saveToken(data.access_token);
      API.setHeader();
      next();
    }).catch((err) => {
      console.error(err)
      next('/login');
    })
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
