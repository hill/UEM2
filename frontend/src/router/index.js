import Vue from "vue";
import VueRouter from "vue-router";
import API from '../services/api.service';
import { AuthService } from '../services/api.service';
import jwtService from "../services/jwt.service";
import store from '../store'

import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Transcript from "../views/Transcript.vue";
import Resources from "../views/Resources.vue";
import Login from "../views/Login.vue";
import NewCourse from "../views/NewCourse.vue";
import Course from "../views/Course.vue";
import Student from "../views/Student.vue";

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
    meta: { requiresAuth: false },
    component: About,
  },
  {
    path: "/student/:studentId",
    name: "Student",
    component: Student,
    meta: { requiresAuth: false },
  },
];

const router = new VueRouter({
  routes,
});

router.beforeResolve((to, from, next) => {
  const token = jwtService.getToken();
  if (token) { API.setHeader(); }
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  // TODO(TOM): refactor this. Try to log in (for the case we go to a page that does not require auth but we could use the user)
  AuthService.verify().then(({data}) => {
    store.commit('setUser', data.user)
  }).catch()


  if (!requiresAuth) {next(); return;}
  // redirect if going to login, already logged in
  if (to.path === '/login') {
		if (token) {
			AuthService.verify().then(() => {
				next('/transcript');
			}).catch(() => {
				next();
			});
		} else {
			next();
		}
	}

  if (token) {
    // Token refresh
    const expiry = JSON.parse(window.atob(token.split('.')[1]))["exp"] * 1000;
    const expiresIn = expiry - new Date().getTime()
    if (expiresIn < 100000 && expiresIn > 0) {
      // request a new token
      AuthService.refresh().then(({data}) => {
        jwtService.saveToken(data.access_token);
        API.setHeader();
        next();
      }).catch((err) => {
        console.error(err)
        next('/login');
      })
    }
  }

  if (requiresAuth && token) {
    // verify the token is valid
    AuthService.verify().then(({data}) => {
      store.commit('setUser', data.user)
      next();
    }).catch(() => {
      console.log("TOKEN INVALID!")
      next('/login');
    });
  } else {
    // you don't have a token!
    next('/login');
  }
});

export default router;
