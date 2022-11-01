import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    showErrorModal: false,
    errorModalContent: "",
    snackbarColor: null,
    showSnackbar: "",
    snackbarText: false,
  },
  getters: {},
  mutations: {
    showErrorModal(state, content) {
      state.errorModalContent = content;
      state.showErrorModal = true;
    },
    setShowErrorModal(state, value) {
      state.showErrorModal = value;
    },
    showSnackbar(state, content) {
      state.snackbarColor = content.color || "success";
      state.snackbarText = content.text;
      state.showSnackbar = true;
    },
    setShowSnackbar(state, value) {
      state.showSnackbar = value;
    },
  },
  actions: {},
});

export default store;
