<template>
  <v-app-bar app>
    <v-app-bar-title
      ><router-link
        :to="{ name: 'FilesTable' }"
        class="text-decoration-none text-dark"
        >FoxMed</router-link
      ></v-app-bar-title
    >

    <v-spacer></v-spacer>
  </v-app-bar>
</template>

<script>
export default {};
</script>

<style>
.v-app-bar-title__content {
  width: 200px !important;
}
</style>