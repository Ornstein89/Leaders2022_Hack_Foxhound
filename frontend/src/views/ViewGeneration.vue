<template>
  <!-- панель инструментов -->
  <!-- <v-toolbar> -->

  <!-- кнопка включения простой разметки -->
  <!-- кнопка включения разметки CVAT-->
  <!-- кнопка сохранения разметки -->
  <!-- </v-toolbar> -->

  <!-- панель управления обзором -->
  <v-row style="height: 100%" no-gutters fill-height>
    <v-col cols="12" sm="9">
      <v-card class="fill-height d-flex flex-column ma-1">
        <!-- само поле просмотра -->
        <!-- <dwvVue /> -->
        <div id="dwv" class="ma-1">
          <!-- <md-progress-bar
            md-mode="determinate"
            :md-value="loadProgress"
          ></md-progress-bar> -->

          <!-- action buttons -->
          <!-- <div class="button-row">
            
            <md-menu md-size="medium" md-align-trigger>
              <md-button
                class="md-raised md-primary"
                md-menu-trigger
                :disabled="!dataLoaded"
              >
                {{ selectedTool }} <md-icon>arrow_drop_down</md-icon></md-button
              >
      
              <md-menu-content>
                <md-menu-item
                  v-for="tool in toolNames"
                  :key="tool"
                  v-on:click="onChangeTool(tool)"
                  >{{ tool }}</md-menu-item
                >
              </md-menu-content>
      
              <md-button
                class="md-raised md-primary"
                v-on:click="onReset()"
                :disabled="!dataLoaded"
                >Reset</md-button
              >
              <md-button
                class="md-raised md-primary"
                v-on:click="showDicomTags = true"
                :disabled="!dataLoaded"
                >Tags</md-button
              >
            </md-menu>

            <md-dialog :md-active.sync="showDicomTags">
              <tagsTable :tagsData="metaData" />
            </md-dialog>
          </div> -->

          <div id="layerGroup0" class="layerGroup">
            <!-- <div id="dropBox"></div> -->
            <div id="infoLayer">
              <div id="infotl" class="infotl info"></div>
              <div id="infotc" class="infotc infoc"></div>
              <div id="infotr" class="infotr info"></div>
              <div id="infocl" class="infocl infoc"></div>
              <div id="infocr" class="infocr infoc"></div>
              <div id="infobl" class="infobl info"></div>
              <div id="infobc" class="infobc infoc"></div>
              <!-- offset for plot -->
              <div id="infobr" class="infobr info" style="bottom: 64px"></div>
              <div id="plot"></div>
              <div id="infocm"></div>
            </div>
          </div>

          <!-- <div class="legend md-caption">
            <p>
              Powered by
              <a href="https://github.com/ivmartel/dwv" title="dwv on github">dwv</a>
              {{ versions.dwv }} and
              <a href="https://github.com/vuejs/vue" title="vue on github">Vue.js</a>
              {{ versions.vue }}
            </p>
          </div> -->
        </div>
      </v-card>
    </v-col>

    <v-col cols="12" sm="3">
      <v-card class="fill-height d-flex flex-column ma-1">
        <v-tabs v-model="tab" align-with-title>
          <v-tabs-slider color="yellow"></v-tabs-slider>

          <v-tab v-for="item in tab_items" :key="item">
            {{ item }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <!-- панель первого генератора на контурах -->
          <v-tab-item>
            <v-card flat class="fill-height d-flex flex-column ma-1">
              <v-card-text>
                <p class="font-weight-black">Генератор аугментаций №1</p>
                <p class="font-weight-bold">Принцип работы:</p>
                <p class="font-italic">
                  1) Генерация случайного гладкого контура неправильной
                  формы;<br />
                  2) Неравномерное сглаживание случайным Гауссовым полем;<br />
                  3) Масштабирование яркости и размера;<br />
                  4) Добавление к исходному изображению;
                </p>
                <p class="font-weight-bold">Особенности:</p>
                <p class="font-italic">
                  1) В настоящий момент генерирует только опухоли
                  (новообразования компактной формы);<br />
                  2) Работает в полуавтоматическом режиме (требует указания
                  положения и размеров от пользователя);
                </p>
              </v-card-text>
              <v-spacer vertical></v-spacer>
              <v-row class="ma-1">
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="x_px"
                    :label="'x, px'"
                    hint="Целое число"
                    persistent-hint
                    prepend-icon="mdi-arrow-right-thin"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="y_px"
                    :label="'y, px'"
                    hint="Целое число"
                    persistent-hint
                    prepend-icon="mdi-arrow-down-thin"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row class="ma-1">
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="width_px"
                    :label="'Ширина, px'"
                    hint="Целое число"
                    persistent-hint
                    prepend-icon="mdi-arrow-left-right-bold"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="height_px"
                    :label="'Высота, px'"
                    hint="Целое число"
                    persistent-hint
                    prepend-icon="mdi-arrow-up-down-bold"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- :rules="[rules.required, rules.date]"
                :readonly="all_readonly" -->

              <v-row class="ma-1">
                <v-btn
                  class="ma-1"
                  color="primary"
                  :loading="loading"
                  @click="onGenerate('simple')"
                  v-if="settingUp"
                >
                  Генерация
                </v-btn>
                <v-btn
                  class="ma-1"
                  color="primary"
                  :loading="loading"
                  @click="onReGenerate('simple')"
                  v-if="!settingUp"
                >
                  Повторная генерация
                </v-btn>
                <v-btn
                  class="ma-1"
                  outlined
                  @click="onSave"
                  :disabled="loading"
                  v-if="!settingUp"
                >
                  <v-icon>mdi-content-save</v-icon>
                  Сохранить
                </v-btn>
                <v-btn
                  class="ma-1"
                  color="error"
                  outlined
                  @click="onCancel"
                  v-if="!settingUp"
                  :disabled="loading"
                >
                  Выход
                </v-btn>
              </v-row>
            </v-card>
          </v-tab-item>

          <!-- панель второго генератора на ML -->
          <v-tab-item>
            <v-card flat class="fill-height d-flex flex-column ma-1">
              <v-card-text>
                <p class="font-weight-black">Генератор аугментаций №1</p>
                <p class="font-weight-bold">Принцип работы:</p>
                <p class="font-italic">
                  1) ...;<br />
                  2) ...;<br />
                  3) ...;<br />
                  4) .;
                </p>
                <p class="font-weight-bold">Особенности:</p>
                <p class="font-italic">
                  1) ...;<br />
                  2) ...;
                </p>
              </v-card-text>
              <v-spacer vertical></v-spacer>
              <v-row class="ma-1">
                <v-btn
                  class="ma-1"
                  color="primary"
                  :loading="loading"
                  @click="onGenerate('pix2pix')"
                  v-if="settingUp"
                >
                  Генерация
                </v-btn>
                <v-btn
                  class="ma-1"
                  color="primary"
                  :loading="loading"
                  @click="onReGenerate('pix2pix')"
                  v-if="!settingUp"
                >
                  Повторная генерация
                </v-btn>
                <v-btn
                  class="ma-1"
                  outlined
                  @click="onSave"
                  :disabled="loading"
                  v-if="!settingUp"
                >
                  <v-icon>mdi-content-save</v-icon>
                  Сохранить
                </v-btn>
                <v-btn
                  class="ma-1"
                  color="error"
                  outlined
                  :disabled="loading"
                  @click="onCancel"
                  v-if="!settingUp"
                >
                  Выход
                </v-btn>
              </v-row>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-col>
  </v-row>
  <!-- диалог генерации -->
</template>
<script>
import http from "../http";

import Vue from "vue";
import dwv from "dwv";

// Vue.use(MdButton);

// gui overrides

// Image decoders (for web workers)
dwv.image.decoderScripts = {
  jpeg2000: "assets/dwv/decoders/pdfjs/decode-jpeg2000.js",
  "jpeg-lossless": "assets/dwv/decoders/rii-mango/decode-jpegloss.js",
  "jpeg-baseline": "assets/dwv/decoders/pdfjs/decode-jpegbaseline.js",
  rle: "assets/dwv/decoders/dwv/decode-rle.js",
};

dwv.tool.defaultpresets = {};

dwv.tool.defaultpresets.CT = {
  mediastinum: { center: 40, width: 400 },
  lung: { center: -500, width: 1500 },
  bone: { center: 500, width: 2000 },
  brain: { center: 40, width: 80 },
  head: { center: 90, width: 350 },
};

export default {
  name: "ViewGeneration",
  data() {
    return {
      //https://ivmartel.github.io/dwv/doc/stable/dwv.tool.html
      toggle_view: null, // состояние панели для управления видом
      toggle_labeling: null, // состояние панели для редактирования
      toggle_labeling_flag: false,
      toggle_view_flag: false,

      versions: {
        dwv: dwv.getVersion(),
        vue: Vue.version,
      },

      dwvApp: null, // библиотека DWV
      infoController: null, // оверлей с информацией о снимке
      infoControllerVisible: false, // состояние оверлея с информацией
      // standardWindows : ["Window1", "Window2", "Lung"],
      selectedStndardWindow: null,
      layergroup: null,
      viewController: null,
      presetNames: null, // пресеты по уровням яркости
      drawColor: "#FF0000",

      isSelecting: false, // для загрузки разметки в json
      selectedFile: null, // файл для загрузки разметки в json

      annotations: {
        objects: [{ x: 1, y: 2 }],
      }, // объекты разметки для перевода в JSON
      tab: null,
      tab_items: ["Генератор 1", "Генератор 2"],
      // номенклатура инструментов https://github.com/ivmartel/dwv-jqui/blob/master/src/applauncher.js
      tools: {
        Scroll: {},
        ZoomAndPan: {},
        WindowLevel: {},
        Draw: {
          options: ["Ruler", "Rectangle", "FreeHand", "Roi"],
          type: "factory",
          events: ["drawcreate", "drawchange", "drawmove", "drawdelete"],
        },
        Livewire: {},
      },
      toolNames: [],
      selectedTool: "Select Tool",
      loadProgress: 0,
      dataLoaded: false,
      metaData: null,
      showDicomTags: false,
      dropboxDivId: "dropBox",
      dropboxClassName: "dropBox",
      borderClassName: "dropBoxBorder",
      hoverClassName: "hover",

      x_px: 150,
      y_px: 250,
      width_px: 30,
      height_px: 30,

      file: null,
      longPoolingInterval: null,
      status: null,
    };
  },
  methods: {
    async checkStatus() {
      this.status = (
        await http.getItem(`/api/files/${this.file.id}/status/`, {
          showSnackbar: true,
        })
      ).data.status;
      if (this.loading) return;
      clearInterval(this.longPoolingInterval);
      this.file = (
        await http.getItem("File", {
          id: this.file.id,
          showSnackbar: true,
        })
      ).data;
      this.dwvApp.reset();
      this.dwvApp.init({
        dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
        tools: this.tools,
      });
      this.dwvApp.loadURLs(this.file.paths);
    },

    async onReGenerate(generator_type) {
      await http.deleteItem("File", { id: this.$route.params.id });
      let params = {};
      if (generator_type == "simple") {
        params = {
          x_px: this.x_px,
          y_px: this.y_px,
          width_px: this.width_px,
          height_px: this.height_px,
        };
      }
      const response = await http.createItem("/api/files/generate/", {
        showSnackbar: true,
        data: {
          origin_path: this.file.origin_path,
          params,
          generator_type,
        },
      });
      if (response.status == 200) {
        this.$router.replace({
          name: "ViewGeneration",
          params: { id: response.data.id },
        });
        await this.reset();
      }
    },

    async onGenerate(generator_type) {
      let params = {};
      const originFileIndex =
        this.viewController.getCurrentIndex().getValues()[2] == -1
          ? 0
          : this.viewController.getCurrentIndex().getValues()[2];
      if (generator_type == "simple") {
        params = {
          x_px: this.x_px,
          y_px: this.y_px,
          width_px: this.width_px,
          height_px: this.height_px,
        };
      }
      const response = await http.createItem("/api/files/generate/", {
        showSnackbar: true,
        data: {
          origin_path: this.file.paths[originFileIndex],
          params,
          generator_type,
        },
      });
      if (response.status == 200) {
        this.$router.replace({
          name: "ViewGeneration",
          params: { id: response.data.id },
        });
        await this.reset();
      }
    },

    onSave() {
      this.$router.replace({
        name: "ViewLabeling",
        params: { id: this.file.id },
      });
    },

    async onCancel() {
      await http.deleteItem("File", { id: this.$route.params.id });
      this.$router.replace({ name: "FilesTable" });
    },

    onChangeTool: function (tool) {
      // при выборе инструмента разметки
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      this.dwvApp.setDrawLineColour(this.drawColor);
    },

    onReset: function () {
      this.dwvApp.resetDisplay();
      this.dwvApp.setTool("Scroll");
      this.toggle_view_flag = true;
      this.toggle_labeling_flag = true;
      this.toggle_labeling = undefined;
      this.toggle_view = undefined;
    },
    async reset() {
      this.file = (
        await http.getItem("File", {
          id: this.$route.params.id,
          showSnackbar: true,
        })
      ).data;
      this.status = this.file.generation_status;
      this.dwvApp.reset();
      this.dwvApp.init({
        dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
        tools: this.tools,
      });
      if (this.file.paths.length) this.dwvApp.loadURLs(this.file.paths);
      else this.longPoolingInterval = setInterval(this.checkStatus, 2000);
    },
  },

  async mounted() {
    this.file = (
      await http.getItem("File", {
        id: this.$route.params.id,
        showSnackbar: true,
      })
    ).data;
    this.status = this.file.generation_status;
    // create app
    this.dwvApp = new dwv.App();
    console.log("mounted(): this.dwvApp = ", this.dwvApp);

    // initialise app
    this.dwvApp.init({
      dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
      tools: this.tools,
    });

    // handle load events
    let nReceivedError = null;
    let nReceivedAbort = null;
    let isFirstRender = null;
    this.dwvApp.addEventListener("loadstart", () => {
      // reset flags
      this.dataLoaded = false;
      nReceivedError = 0;
      nReceivedAbort = 0;
      isFirstRender = true;
    });
    this.dwvApp.addEventListener("loadprogress", (event) => {
      this.loadProgress = event.loaded;
    });
    this.dwvApp.addEventListener("renderend", (/*event*/) => {
      if (isFirstRender) {
        isFirstRender = false;
        // available tools
        this.toolNames = [];
        for (const key in this.tools) {
          if (
            (key === "Scroll" && this.dwvApp.canScroll()) ||
            (key === "WindowLevel" && this.dwvApp.canWindowLevel()) ||
            (key !== "Scroll" && key !== "WindowLevel")
          ) {
            this.toolNames.push(key);
          }
        }
        this.onChangeTool(this.toolNames[0]);
        console.log("mounted(): toolNames = ", this.toolNames);
      }
    });
    this.dwvApp.addEventListener("load", (/*event*/) => {
      // set dicom tags
      this.metaData = dwv.utils.objectToArray(this.dwvApp.getMetaData(0));
      // set data loaded flag
      this.dataLoaded = true;
    });
    this.dwvApp.addEventListener("loadend", (/*event*/) => {
      if (nReceivedError) {
        this.loadProgress = 0;
        // alert("Received errors during load. Check log for details.");
        // show drop box if nothing has been loaded
      }
      if (nReceivedAbort) {
        this.loadProgress = 0;
        alert("Load was aborted.");
      }

      this.layergroup = this.dwvApp.getActiveLayerGroup();
      this.viewController = this.layergroup
        .getActiveViewLayer()
        .getViewController();

      console.log("layer group = ", this.layergroup);
      console.log("viewController = ", this.viewController);
      console.log("presetNames = ", this.presetNames);

      // dwv.setDrawLineColour('Red');
      // console.log("layer group = ", this.dwvApp.getActiveLayerGroup());
    });
    this.dwvApp.addEventListener("loaditem", (event) => {
      if (event.loadtype === "image") {
        //
      }
    });
    this.dwvApp.addEventListener("error", (/*event*/) => {
      // console.error('load error', event)
      ++nReceivedError;
    });
    this.dwvApp.addEventListener("abort", (/*event*/) => {
      ++nReceivedAbort;
    });

    // handle key events
    this.dwvApp.addEventListener("keydown", (event) => {
      this.dwvApp.defaultOnKeydown(event);
    });
    // handle window resize
    window.addEventListener("resize", this.dwvApp.onResize);

    // possible load from location
    dwv.utils.loadFromUri(window.location.href, this.dwvApp);
    console.log("dwv = ", dwv);
    console.log("dwvApp = ", this.dwvApp);
    if (this.file.paths.length) this.dwvApp.loadURLs(this.file.paths);
    else this.longPoolingInterval = setInterval(this.checkStatus, 2000);
  },
  computed: {
    settingUp() {
      return this.$route.name == "ViewGenerationSetup";
    },
    loading() {
      return this.status == "processing";
    },
  },
  beforeDestroy() {
    clearInterval(this.longPoolingInterval);
  },
  watch: {
    toggle_view: function (tool) {
      if (this.toggle_view_flag) {
        this.toggle_view_flag = false;
        return;
      }
      console.log("toggle_view changed, arg=", tool);
      if (tool == undefined) {
        // this.dwvApp.setTool('Scroll');
        this.selectedTool = "Scroll";
        return;
      }
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      this.toggle_labeling = undefined; //TODO
      this.toggle_labeling_flag = true;
    },

    toggle_labeling: function (shape) {
      // при выборе инструмента разметки

      if (this.toggle_labeling_flag) {
        this.toggle_labeling_flag = false;
        return;
      }
      console.log("toggle_labeling changed, tool=", shape);

      // нажата кнопка сброса
      if (shape == undefined) {
        this.selectedTool = "Scroll";
        return;
      }

      //деактивация противоположной панели
      this.toggle_view = undefined; //TODO
      this.toggle_view_flag = true;

      if (shape === "Livewire") {
        this.selectedTool = "Livewire";
        this.dwvApp.setTool("Livewire");
        this.dwvApp.setDrawLineColour(this.drawColor);
        return;
      }

      // активация команды
      console.log("1. before selectedTool");
      this.selectedTool = "Draw";
      this.dwvApp.setTool("Draw");
      console.log("toggle_labeling(), shape = ", shape);
    },
  },
};
</script>

<!-- <style scoped>
.v-btn-toggle {
  flex-direction: column;
}
</style> -->

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#dwv {
  /*font-family: Arial, Helvetica, sans-serif;*/
  height: 100%;
  /*width: 100%;
  border: 3px;
  border-color: lightgrey;*/
}

.button-row {
  text-align: center;
  padding: 5px;
}

#dwv button {
  margin: 2px;
}

/* Layers */
.layerGroup {
  position: relative;
  padding: 0;
  display: flex;
  justify-content: center;
  height: 95%;
}
.layer {
  position: absolute;
  pointer-events: none;
}

/* drag&drop */
.dropBox {
  margin: auto;
  text-align: center;
  vertical-align: middle;
  width: 50%;
  height: 75%;
}
.dropBoxBorder {
  border: 5px dashed rgba(68, 138, 255, 0.38);
}
.dropBoxBorder.hover {
  border: 5px dashed var(--md-theme-default-primary);
}

.md-dialog {
  width: 80%;
  height: 90%;
}

/* Info */
#infoLayer {
  position: absolute;
  pointer-events: none;
  z-index: 20;
  width: 100%;
  height: 100%;
}
#infoLayer ul {
  margin: 0;
  padding: 2px;
  list-style-type: none;
}
#infoLayer li {
  margin-top: 0;
}
#infoLayer canvas {
  margin: 0;
  padding: 2px;
}
.info {
  color: #cde;
  text-shadow: 1px 1px #000;
  font-size: 80%;
}
.infoc {
  color: #ff0;
  text-shadow: 1px 1px #000;
  font-size: 120%;
}
.infotl {
  position: absolute;
  top: 0;
  left: 0;
  text-align: left;
}
.infotc {
  position: absolute;
  top: 0;
  left: 50%;
  right: 50%;
  text-align: center;
}
.infotr {
  position: absolute;
  top: 0;
  right: 0;
  text-align: right;
}
.infocl {
  position: absolute;
  bottom: 50%;
  left: 0;
  text-align: left;
}
.infocr {
  position: absolute;
  bottom: 50%;
  right: 2px;
  text-align: right;
}
.infobl {
  position: absolute;
  bottom: 0;
  left: 0;
  text-align: left;
}
.infobc {
  position: absolute;
  bottom: 0;
  left: 50%;
  right: 50%;
  text-align: center;
}
.infobr {
  position: absolute;
  bottom: 0;
  right: 0;
  text-align: right;
}

#plot {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 15px;
  right: 0;
}
#infocm {
  position: absolute;
  bottom: 5px;
  right: 0;
}
</style>
<!-- non "scoped" style -->
<style>
.layer {
  position: absolute;
  pointer-events: none;
}
</style>