import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import JwtService from "./jwt.service"

const API_URL = "http://localhost:5000"

const instance = axios.create({baseURL: API_URL})

const API = {
  init: () => {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;

    // Vue.axios.interceptors.request.use(
    //   (config) => {
    //     return new Promise((resolve, reject) => {
    //       // try {
    //         CognitoAuth.getIdToken((err, jwtToken) => {
    //           if (err) {
    //             console.log("Cognito auth error");
    //             reject(err);
    //           }
    //           config.headers = { Authorization: jwtToken.id_token };
    //           return resolve(config);
    //         });
    //     });
    //   },
    //   (err) => {
    //     console.error(err);
    //   }
    // );
  },
  setHeader: () => {
    Vue.axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${JwtService.getToken()}`;
  },
  get: (url, params) => {
    return Vue.axios.get(url, params)
  },
  post: (url, params) => {
    return Vue.axios.post(url, params)
  },
  put: (url, params) => {
    return Vue.axios.put(url, params)
  },
  delete: (url, params) => {
    return Vue.axios.delete(url, params)
  }
};

export default API;

export const CourseService = {
  list: () => {
    return API.get("/course/")
  },
  get: (id) => {
    return API.get(`/course/${id}`)
  },
  create: (name, description, due) => {
    return API.post(`/course/create`, {name, description, due})
  },
  update: (name, description, due) => {
    return API.put(`/course/${id}`, {name, description, due})
  },
  delete: (id) => {
    return API.delete(`/course/${id}`)
  }
}