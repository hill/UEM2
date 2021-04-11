import Vue from "vue";
import Vuex from "vuex";
import JwtService from '../services/jwt.service'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
  },
  mutations: {
    setUser: (state, user) => {
      state.user = user;
    },
    purgeAuth: (state) => {
      state.user = null;
      JwtService.destroyToken();
    },
  },
  actions: {
    // login: async ({ dispatch, state }, { email, password }) => {
    //   try {
    //     await Auth.signIn(email, password);
    //   } catch (err) {
    //     console.error(`[Login Error] ${err}`);
    //   }
    // },
    // signup: async ({ dispatch, state }, { email, password }) => {
    //   try {
    //     await Auth.signIn(email, password);
    //   } catch (err) {
    //     console.error(`[Login Error] ${err}`);
    //   }
    // },
    updateUser: ({ commit }, user) => {
      commit("setUser", user);
    },
    logout: ({ commit }) => {
      commit("purgeAuth");
    },
  },
  modules: {},
});
