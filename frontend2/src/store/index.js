import Vue from "vue";
import Vuex from "vuex";
import JwtService from "../services/jwt.service";
import API, { AuthService } from "../services/api.service";

Vue.use(Vuex);

// TODO(TOM): refactor

export const store = new Vuex.Store({
  state: {
    user: null,
    token: "",
  },
  mutations: {
    authUser: (state, user) => {
      state.user = user;
    },
    purgeAuth: (state) => {
      state.user = null;
      JwtService.destroyToken();
    },
    setUser: (state, user) => {
      state.user = user;
    },
  },
  actions: {
    // When you need an asynchronous action alongside a mutation
    signup: ({ commit }, authCreds) => {
      return new Promise((resolve, reject) => {
        AuthService.register(
          authCreds.name,
          authCreds.email,
          authCreds.password
        )
          .then(({ data }) => {
            resolve(data);
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    login: ({ commit }, authCreds) => {
      return new Promise((resolve, reject) => {
        AuthService.login(authCreds.email, authCreds.password)
          .then(({ data }) => {
            JwtService.saveToken(data.access_token);
            API.setHeader();
            AuthService.getMe()
              .then(({ data }) => {
                commit("authUser", data);
              })
              .catch((err) => {
                console.log("reject getMe with ", err);
              });
            resolve(data);
          })
          .catch((err) => {
            console.log("reject with ", err);
            reject(err);
          });
      });
    },
    updateUser: ({ commit }, user) => {
      // technically don't need this...not doing async work.
      commit("setUser", user);
    },
    logout: ({ commit }) => {
      commit("purgeAuth");
    },
  },
  modules: {},
});
