<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      hide-default-footer
      :items-per-page="-1"
      class="elevation-1"
      fixed-header
      height="89vh"
      :loading="loading"
      must-sort
      :sort-by.sync="order"
      :sort-desc.sync="desc"
      :custom-sort="(items) => items"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Файлы</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            outlined
            dense
            label="Поиск"
            append-outer-icon="mdi-magnify"
            @click:append-outer="doSearch"
            @keyup.enter="doSearch"
          /> </v-toolbar
      ></template>
      <template v-slot:item.preview="{ item }">
        <v-img contain :src="item.preview" height="128" v-if="item.preview" />
      </template>
      <template v-slot:item.download="{ item }">
        <v-btn
          icon
          :disabled="!item.is_marked_up"
          @click="downloadMarkup(item)"
          :loading="item.loading"
        >
          <v-icon class="mr-2"> mdi-download </v-icon>
        </v-btn>
      </template>
      <template v-slot:item.is_marked_up="{ item }">
        <v-icon class="mr-2" :color="item.is_marked_up ? 'green' : 'red'">
          {{
            item.is_marked_up
              ? "mdi-checkbox-marked-circle"
              : "mdi-close-circle"
          }}
        </v-icon>
      </template>
      <template v-slot:item.origin_path="{ item }">
        <v-icon class="mr-2" :color="item.origin_path ? 'green' : 'red'">
          {{
            item.origin_path ? "mdi-checkbox-marked-circle" : "mdi-close-circle"
          }}
        </v-icon>
      </template>
      <template v-slot:item.dttm_created="{ item }">
        <span>{{ getDate(item.dttm_created) }}</span>
      </template>
      <template v-slot:item.dttm_updated="{ item }">
        <span>{{ getDate(item.dttm_updated) }}</span>
      </template>
      <template v-slot:body.append>
        <v-card v-intersect="fetchData" v-if="!allDataLoaded"
          ><v-card-title></v-card-title
        ></v-card>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import http from "@/http";
import Axios from "axios";
export default {
  data() {
    return {
      loading: false,
      offset: 0,
      order: "dttm_updated",
      desc: true,
      search: "",
      headers: [
        {
          text: "Предпросмотр",
          value: "preview",
          align: "center",
          sortable: false,
        },
        { text: "Название", value: "name", align: "center" },
        { text: "Создано", value: "dttm_created", align: "center" },
        { text: "Обновлено", value: "dttm_updated", align: "center" },
        {
          text: "Есть разметка",
          value: "is_marked_up",
          align: "center",
          sortable: false,
        },
        {
          text: "Сгенерирован системой",
          value: "origin_path",
          align: "center",
          sortable: false,
        },
        {
          text: "Скачать JSON",
          value: "download",
          align: "center",
          sortable: false,
        },
      ],
      items: [],
      allDataLoaded: false,
    };
  },
  methods: {
    async fetchData(entries, observer, isIntersecting) {
      if (this.loading || !isIntersecting) return;
      await this.loadItems();
    },
    async loadItems() {
      this.loading = true;
      const response = await http.getList("File", {
        showSnackbar: true,
        filters: {
          limit: 20,
          offset: this.offset,
          order: this.orderBy,
          search: this.search,
        },
      });
      this.items = [...this.items, ...response.data];
      this.offset += 20;
      if (!response.data.length) this.allDataLoaded = true;
      this.loading = false;
    },
    async downloadMarkup(item) {
      item.loading = true;
      const response = await Axios.get(`/api/files/${item.id}/markup/`, {
        responseType: "blob",
      });
      const blob = new Blob([response.data], { type: "application/json" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = item.name + "_markup.json";
      link.click();
      URL.revokeObjectURL(link.href);
      item.loading = false;
    },
    getDate(date) {
      return new Date(date).toLocaleString();
    },
    doSearch() {
      this.offset = 0;
      this.allDataLoaded = false;
      this.items = [];
    },
  },
  computed: {
    infiniteScrollDisabled() {
      return this.loading || this.allDataLoaded;
    },
    orderBy() {
      return this.desc ? "-" + this.order : this.order;
    },
  },
  watch: {
    orderBy() {
      this.offset = 0;
      this.allDataLoaded = false;
      this.items = [];
    },
  },
};
</script>
<style>
</style>