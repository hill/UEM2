import Vue from "vue";
import Vuex from "vuex";
import JwtService from '../services/jwt.service'
import API from '../services/api.service'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
  },
  mutations: {
    authUser: (state, {user, access_token}) => {
      state.user = user;
      JwtService.saveToken(access_token);
      API.setHeader();
    },
    purgeAuth: (state) => {
      state.user = null;
      JwtService.destroyToken();
    },
    setUser: (state, user) => {
      state.user = user
    }
  },
  actions: {
    // When you need an asynchronous action alongside a mutation
    signup: ({commit}, authCreds) => {
      return new Promise((resolve, reject) => {
        API.post("/auth/register", { email: authCreds.email, password: authCreds.password, name: authCreds.name })
          .then(({ data }) => {
            commit('authUser', data);
            resolve(data);
          })
          .catch((err) => {
            reject(err)
          });
      });
    },
    login: ({commit}, authCreds) => {
      return new Promise((resolve, reject) => {
        API.post("/auth/login", { email: authCreds.email, password: authCreds.password })
          .then(({ data }) => {
            commit('authUser', data);
            resolve(data);
          })
          .catch((err) => {
            console.log('reject with ', err)
            reject(err);
          });
      });
    },
    updateUser: ({ commit }, user) => { // technically don't need this...not doing async work.
      commit("setUser", user);
    },
    logout: ({ commit }) => {
      commit("purgeAuth");
    },
  },
  modules: {},
});
