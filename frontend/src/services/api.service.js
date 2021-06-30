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
  list: () => API.get("/course/"),
  get: (id) => API.get(`/course/${id}`),
  create: (name, description, due) => API.post(`/course/create`, {name, description, due}),
  update: (name, description, due) => API.put(`/course/${id}`, {name, description, due}),
  delete: (id) => API.delete(`/course/${id}`),
}

export const ResourceService = {
  list: () => API.get("/resource/"),
  get: (id) => API.get(`/resource/${id}`),
  create: (name, url, topics) => API.post(`/resource/create`, {name, url, topics}),
  find: (searchTerm) => API.get(`/resource/?search=${searchTerm}`),
  upvote: (resourceId) => API.post(`/resource/${resourceId}/upvote`),
  downvote: (resourceId) => API.post(`/resource/${resourceId}/downvote`),
  broken: (resourceId) => API.post(`/resource/${resourceId}/broken`)
}

export const TopicService = {
  list: () => API.get("/resource/topics")
}