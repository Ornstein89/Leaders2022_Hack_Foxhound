<template>
  <v-card>
    <v-card-title>Загрузка DICOM файла</v-card-title>
    <v-card-text>
      <v-form v-model="valid" enctype="multipart/form-data">
        <v-text-field
          label="Название"
          :rules="rules"
          v-model="name"
          :loading="loading"
        />
        <v-file-input
          accept=".dcm"
          label="DICOM файлы"
          :rules="rules"
          v-model="files"
          :loading="loading"
          multiple
          show-size
          counter
        />
        <v-btn :disabled="!valid" @click="load" :loading="loading"
          >Загрузить</v-btn
        >
      </v-form>
    </v-card-text>
  </v-card>
</template>
<script>
import Vue from "vue";
import { required } from "@/validators";
import axios from "axios";
import { mapMutations } from "vuex";
export default Vue.extend({
  data() {
    return {
      valid: false,
      rules: [required],
      files: [],
      loading: false,
      name: "",
    };
  },
  methods: {
    ...mapMutations(["showSnackbar"]),
    async load() {
      if (!this.files.length) return;
      this.loading = true;
      const form = new FormData();
      for (const file of this.files) form.append("files", file);
      form.append("name", this.name);
      try {
        const response = await axios.post("/api/files/", form);
        this.showSnackbar({
          text: "Файл успешно загружен",
        });
        this.$router.push({
          name: "ViewLabeling",
          params: { id: response.data.id },
        });
      } catch (error) {
        this.showSnackbar({
          text: error.response.data.detail || "Что-то пошло не так",
          color: "warning",
        });
      }
      this.loading = false;
    },
  },
});
</script>
<style>
</style>