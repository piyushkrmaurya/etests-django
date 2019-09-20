import { batchService } from "@/api/batch.service";

const initialState = {
  status: {},
  batch: {},
  items: []
};

export const batches = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);

      batchService.get(id).then(
        batch => {
          commit("getSuccess", batch);
          setTimeout(() => {
            dispatch("alert/success", "Batch fetched successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    create({ dispatch, commit }, data) {
      commit("createRequest", data);

      batchService.create(data).then(
        data => {
          commit("createSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Batch created successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("createFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    update({ dispatch, commit }, data) {
      commit("updateRequest", data);

      batchService.update(data).then(
        data => {
          commit("updateSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Batch update successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("updateFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    join({ dispatch, commit }, data) {
      commit("joinRequest", data.rollNumber);

      batchService.join(data).then(
        _ => {
          commit("joinSuccess", data.rollNumber);
          setTimeout(() => {
            dispatch("alert/success", "Joined successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("joinFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    newEnrollments({ dispatch, commit }, data) {
      commit("newEnrollmentsSuccess", data);
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      batchService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Batch removed successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("removeFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    removeStudent({ dispatch, commit }, id) {
      commit("removeStudentSuccess", id);
    },
    list({ commit }) {
      commit("listRequest");

      batchService
        .list()
        .then(
          batches => commit("listSuccess", batches),
          error => commit("listFailure", error)
        );
    },
    detailedList({ commit }) {
      commit("detailedListRequest");

      batchService
        .detailedList()
        .then(
          batches => commit("detailedListSuccess", batches),
          error => commit("detailedListFailure", error)
        );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, batch) {
      state.status = {};
      state.batch = batch;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    listRequest(state) {
      state.status = { loading: true };
    },
    listSuccess(state, batches) {
      state.items = batches;
    },
    listFailure(state, error) {
      state.status = { error };
    },
    detailedListRequest(state) {
      state.status = { loading: true };
    },
    detailedListSuccess(state, batches) {
      state.items = batches;
    },
    detailedListFailure(state, error) {
      state.status = { error };
    },
    createRequest(state, data) {
      state.status = { creating: true };
    },
    createSuccess(state, data) {
      state.status = { created: true, batch: data };
      state.items.push(data);
    },
    createFailure(state, error) {
      state.status = { error: error };
    },
    updateRequest(state, data) {
      state.status = { creating: true };
    },
    updateSuccess(state, data) {
      state.status = { created: true, batch: data };
    },
    updateFailure(state, error) {
      state.status = { error: error };
    },
    joinRequest(state, id) {
      state.status = { joining: true, id: id };
    },
    joinSuccess(state, id) {
      state.status = { joined: true, id: id };
    },
    joinFailure(state, error) {
      state.status = { error: error };
    },
    newEnrollmentsSuccess(state, data) {
      var index = state.items.findIndex(item => item.id === data.batchId);
      console.log(index, data.batchId, state.items);
      if (index >= 0)
        data.enrollments.forEach(e => {
          state.items[index].enrollments.push(e);
        });
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
      state.items = state.items.filter(batch => batch.id !== id);
    },
    removeFailure(state, error) {
      state.status = { error: error };
    },
    removeStudentSuccess(state, id) {
      state.items.forEach((item, i) => {
        var index = item.enrollments.findIndex(e => e.id === id);
        if (index >= 0) item.enrollments.splice(index, 1);
      });
    }
  }
};