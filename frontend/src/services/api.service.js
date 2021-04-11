import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import JwtService from "./jwt.service"

API_URL = "http://localhost:8000"

const instance = axios.create({baseURL: API_URL})

const API = {
  init: () => {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;

    Vue.axios.interceptors.request.use(
      (config) => {
        return new Promise((resolve, reject) => {
          // try {
            CognitoAuth.getIdToken((err, jwtToken) => {
              if (err) {
                console.log("Cognito auth error");
                reject(err);
              }
              config.headers = { Authorization: jwtToken.id_token };
              return resolve(config);
            });
        });
      },
      (err) => {
        console.error(err);
      }
    );
  },
  setHeader: () => {
    Vue.axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${JwtService.getToken()}`;
  },
  get: (url, params) => {
    return Vue.axios.get(url, params).catch((err) => {
      throw new Error(`[API] Error ${err}`);
    });
  },
  post: (url, params) => {
    return Vue.axios.post(url, params).catch((err) => {
      throw new Error(`[API] Error ${err}`);
    });
  },
  put: (url, params) => {
    return Vue.axios.put(url, params).catch((err) => {
      throw new Error(`[API] Error ${err}`);
    });
  },
  delete: (url, params) => {
    return Vue.axios.delete(url, params).catch((err) => {
      throw new Error(`[API] Error ${err}`);
    });
  }
};

export default API;
