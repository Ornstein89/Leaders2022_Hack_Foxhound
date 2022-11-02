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
      @click:row="viewAndLabeling"
    >
      <template
        v-slot:item.preview="{ item }"
      >
        <v-img contain :src="item.preview" height="256"></v-img>
      </template>
      <template v-slot:item.download="{ item }">
        <v-icon class="mr-2" @click="downloadJSON(item)">
          mdi-download
        </v-icon>
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
            item.origin_path
              ? "mdi-checkbox-marked-circle"
              : "mdi-close-circle"
          }}
        </v-icon>
      </template>
      <template v-slot:body.append>
        <v-card v-intersect="fetchData" v-if="!allDataLoaded"><v-card-title></v-card-title></v-card>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import http from "@/http";
export default {
  data() {
    return {
      loading: false,
      offset: 0,
      headers: [
        { text: "Предпросмотр", value: "preview", align: "center" },
        { text: "Название", value: "name", align: "center" },
        { text: "Создано", value: "dttm_created", align: "center" },
        { text: "Обновлено", value: "dttm_updated", align: "center" },
        { text: "Есть разметка", value: "is_marked_up", align: "center" },
        { text: "Сгенерирован системой", value: "origin_path", align: "center" },
        { text: "Скачать JSON", value: "download", align: "center" },
      ],
      items: [
        {
          id:1,
          preview:"1-01.png",
          download:"1-01.png",
          is_marked_up:false,
          origin_path:"1-01.png"
        }
      ],
      allDataLoaded: false,
    };
  },
  methods: {
    async fetchData(entries, observer, isIntersecting) {
        console.log(isIntersecting);
      if (this.loading || !isIntersecting) return;
      this.loading = true;
      const response = await http.getList("File", {
        showSnackbar: true,
        filters: { limit: 10, offset: this.offset },
      });
      this.items = [...this.items, ...response.data];
      this.offset += 10;
      if (!response.data.length) this.allDataLoaded = true;
      this.loading = false;
    },

    viewAndLabeling(item){
      console.log("viewAndLabeling(): row = ", item);
      this.$router.push({
        name:"ViewLabeling",
        params:{id:item.id},
      })
    },
  },
  computed: {
    infiniteScrollDisabled() {
      return this.loading || this.allDataLoaded;
    },
  },
};
</script>
<style>
</style>
