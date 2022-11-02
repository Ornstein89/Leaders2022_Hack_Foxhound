<template>
  <!-- панель инструментов -->
  <!-- <v-toolbar> -->
  <!-- панель управления обзором -->
  <!-- кнопка включения простой разметки -->
  <!-- кнопка включения разметки CVAT-->
  <!-- кнопка сохранения разметки -->
  <!-- </v-toolbar> -->

  <v-row style="height: 100%" no-gutters fill-height>
    <v-col cols="12" sm="1">
      <v-card class="fill-height d-flex flex-column  ma-1">
        v-btn
      </v-card>
    </v-col>
    <v-col cols="12" sm="10">
      <v-card class="fill-height d-flex flex-column  ma-1">
        <!-- само поле просмотра -->
        
      </v-card>
    </v-col>
    <v-col cols="12" sm="1">
        <v-card class="fill-height d-flex flex-column ma-1">
            v-btn
          </v-card>
    </v-col>
    
  </v-row>
  <!-- диалог генерации -->
</template>

<script>
// import http from "@/http";
export default {
  name: "ViewLabeling",
  data() {
    return {};
  },
  methods: {},
  mounted() {
    console.log("mounted(): id = ", this.$route.params.id);
    // TODO загрузка файла по ID
  },
  computed: {},
};
</script>