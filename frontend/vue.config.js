module.exports = {
  transpileDependencies: ["vuetify"],
  devServer: {
    proxy: "http://158.160.36.137",
    // proxy: "http://localhost:8081",
  },
  configureWebpack: {
    devtool: "source-map",
  },
};
