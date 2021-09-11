import axios from "axios";
import JwtService from "./jwt.service";

const API_URL = "http://localhost:8000/api/v1";

const instance = axios.create({ baseURL: API_URL });

const API = {
  setHeader: () => {
    instance.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${JwtService.getToken()}`;
  },
  get: (url, params) => {
    return instance.get(url, params);
  },
  post: (url, params) => {
    return instance.post(url, params);
  },
  put: (url, params) => {
    return instance.put(url, params);
  },
  patch: (url, params) => {
    return instance.patch(url, params);
  },
  delete: (url, params) => {
    return instance.delete(url, params);
  },
};

export default API;

export const AuthService = {
  login: (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);
    return API.post("/auth/login/access-token", params);
  },
  register: (name, email, password) => {
    API.post("/users/", { name, email, password });
  },
  verify: () => API.post("/auth/login/test-token"),
  getMe: () => API.get("/users/me"),
  refresh: () => API.post("/auth/refresh"),
};

export const CourseService = {
  list: () => API.get("/courses/"),
  get: (id) => API.get(`/courses/${id}`),
  create: (name, description, due, syllabus) => {
    console.log({ name, description, due, syllabus });
    return API.post(`/courses/`, { name, description, due, syllabus });
  },
  update: (id, name, description, due, syllabus) =>
    API.patch(`/courses/${id}`, { name, description, due, syllabus }), // TODO(TOM): wrap args in obj?
  delete: (id) => API.delete(`/courses/${id}`),
};

export const ResourceService = {
  list: () => API.get("/resources/"),
  get: (id) => API.get(`/resources/${id}`),
  create: (name, url, topics) => API.post(`/resources/`, { name, url, topics }),
  find: (searchTerm) => API.get(`/resources/?search=${searchTerm}`),
  upvote: (resourceId) => API.patch(`/resources/${resourceId}/vote?vote=1`),
  downvote: (resourceId) => API.patch(`/resources/${resourceId}/vote?vote=-1`),
  broken: (resourceId) => API.patch(`/resources/${resourceId}/broken`),
};

export const TopicService = {
  list: () => API.get("/topics/"),
  create: (name) => API.post("/topics/", { name }),
};