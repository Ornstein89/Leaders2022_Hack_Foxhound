module.exports = {
  transpileDependencies: ["vuetify"],
  devServer: {
    proxy: "http://158.160.36.137",
  },
  configureWebpack: {
    devtool: "source-map",
  },
};
