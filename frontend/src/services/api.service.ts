import axios, { AxiosRequestConfig } from "axios";
import { Resource } from "../types/Resource";
import JwtService from "./jwt.service";

const API_URL = "http://localhost:8000";

const instance = axios.create({ baseURL: API_URL });

const API = {
  setHeader: () => {
    instance.defaults.headers.common["Authorization"] = `Bearer ${JwtService.getToken()}`;
  },
  get: <T>(url: string, params?: object) => instance.get<T>(url, params),
  post: <T>(url: string, params?: object) => instance.post<T>(url, params),
  put: <T>(url: string, params?: object) => instance.put<T>(url, params),
  patch: <T>(url: string, params?: object) => instance.patch<T>(url, params),
  delete: <T>(url: string, params?: object) => instance.delete<T>(url, params),
};

export default API;

type LoginResponse = {
  access: string;
  refresh: string;
};

type RefreshResponse = {
  access: string;
};

export const AuthService = {
  login: (username: string, password: string) => {
    return API.post<LoginResponse>("/api/token", { username, password });
  },
  register: (username: string, email: string, password: string) => {
    API.post("/api/signup", { username, email, password });
  },
  verify: () => {
    const token = JwtService.getToken();
    if (token) {
      return API.post("/api/token/verify/", { token });
    }
    return Promise.resolve({ data: false });
  },
  //getMe: () => API.get("/users/me"),
  getMe: () => ({}),
  refresh: () =>
    API.post<RefreshResponse>("/api/token/refresh/", { refresh: JwtService.getRefreshToken() }),
  //getSetupIntentSecret: () => API.post("/util/create-setup-intent"),
};

// TODO(TOM): typescript?
// export const CourseService = {
//   list: () => API.get("/courses/"),
//   get: (id) => API.get(`/courses/${id}`),
//   create: (
//     name,
//     code,
//     description,
//     primary_resource,
//     due,
//     syllabus,
//     assessments,
//     status,
//     cover_color
//   ) => {
//     return API.post(`/courses/`, {
//       name,
//       code,
//       description,
//       primary_resource,
//       due,
//       syllabus,
//       assignments: assessments,
//       cover: { color: cover_color },
//       status,
//     });
//   },
//   update: (id, name, description, due, syllabus) =>
//     API.patch(`/courses/${id}`, { name, description, due, syllabus }), // TODO(TOM): wrap args in obj?
//   delete: (id) => API.delete(`/courses/${id}`),
// };
export const CourseService = {};

export const ResourceService = {
  list: () => API.get<Resource[]>("/resources/"),
  get: (id: string) => API.get(`/resources/${id}`),
  create: (name: string, url: string, topics: string) =>
    API.post(`/resources/`, { name, url, topics }),
  find: (searchTerm: string) => API.get(`/resources/?search=${searchTerm}`),
  upvote: (resourceId: string) => API.patch(`/resources/${resourceId}/vote?vote=1`),
  downvote: (resourceId: string) => API.patch(`/resources/${resourceId}/vote?vote=-1`),
  broken: (resourceId: string) => API.patch(`/resources/${resourceId}/broken`),
};

export const TopicService = {
  // list: () => API.get("/topics/"),
  // create: (name) => API.post("/topics/", { name }),
  list: () => Promise.resolve([]),
};
