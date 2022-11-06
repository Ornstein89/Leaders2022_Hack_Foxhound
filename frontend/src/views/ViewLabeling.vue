<template>
  <!-- панель инструментов -->
  <!-- <v-toolbar> -->

  <!-- кнопка включения простой разметки -->
  <!-- кнопка включения разметки CVAT-->
  <!-- кнопка сохранения разметки -->
  <!-- </v-toolbar> -->

  <!-- панель управления обзором -->
  <v-row style="height: 100%" no-gutters fill-height>
    <v-col cols="12" sm="1">
      <v-card class="fill-height d-flex flex-column ma-1">
        <v-spacer vertical></v-spacer>

        <v-btn class="ma-1" tile elevation="0" outlined @click="onReset">
          <v-icon>mdi-border-radius</v-icon>
        </v-btn>

        <v-btn-toggle v-model="toggle_view" style="flex-direction: column" tile>
          <v-btn class="ma-1" :value="'ZoomAndPan'">
            <v-icon>mdi-magnify</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'WindowLevel'">
            <v-icon>mdi-weather-sunny</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Scroll'">
            <v-icon>mdi-contrast-circle</v-icon>
          </v-btn>

          <v-btn class="ma-1" disabled>
            <v-icon>mdi-layers-triple-outline</v-icon>
          </v-btn>
        </v-btn-toggle>

        <v-spacer vertical></v-spacer>
      </v-card>
    </v-col>

    <v-col cols="12" sm="10">
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
    <v-col cols="12" sm="1">
      <v-card class="fill-height d-flex flex-column ma-1">
        <v-spacer vertical></v-spacer>

        <v-btn-toggle
          v-model="toggle_labeling"
          style="flex-direction: column"
          tile
        >
          <v-btn class="ma-1" :value="'Ruler'">
            <v-icon>mdi-ruler</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Rectangle'">
            <v-icon>mdi-vector-rectangle</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Roi'">
            <v-icon>mdi-vector-polygon</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'FreeHand'">
            <v-icon>mdi-vector-radius</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Livewire'">
            <v-icon>mdi-draw</v-icon>
          </v-btn>
        </v-btn-toggle>

        <v-btn class="ma-1" tile disabled elevation="0">
          <v-icon>mdi-content-save</v-icon>
        </v-btn>

        <v-btn class="ma-1" tile disabled elevation="0">
          <v-icon>mdi-download</v-icon>
        </v-btn>

        <v-spacer vertical></v-spacer>

        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              v-bind="attrs"
              v-on="on"
              color="primary"
            >
              <!-- <v-avatar color="primary"> -->
              <!-- <img src="https://github.com/opencv/cvat/blob/develop/site/content/en/images/logo2.png?raw=true"> -->
              <img
                width="50"
                src="https://uploads-ssl.webflow.com/62bebfb83044de7f13ae257e/62bec02423796903b293473e_Logo.svg"
              />
              <!-- </v-avatar> -->
            </v-btn>
          </template>
          <span>Экспериментальная интеграция CVAT</span>
        </v-tooltip>
      </v-card>
    </v-col>
  </v-row>
  <!-- диалог генерации -->
</template>

<script>
import http from "@/http";
// import dwvVue from 'dwv';
// import dwvVue from '../components/dwv';

import Vue from "vue";
import dwv from "dwv";
// import tagsTable from '../components/tags-table.vue'
// gui overrides

// Image decoders (for web workers)
dwv.image.decoderScripts = {
  jpeg2000: "assets/dwv/decoders/pdfjs/decode-jpeg2000.js",
  "jpeg-lossless": "assets/dwv/decoders/rii-mango/decode-jpegloss.js",
  "jpeg-baseline": "assets/dwv/decoders/pdfjs/decode-jpegbaseline.js",
  rle: "assets/dwv/decoders/dwv/decode-rle.js",
};

export default {
  name: "ViewLabeling",
  components: {
    // dwvVue,
    // tagsTable,
  },
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
      dwvApp: null,
      tools: {
        Scroll: {},
        ZoomAndPan: {},
        WindowLevel: {},
        Draw: {
          options: ["Ruler", "Rectangle", "FreeHand", "Roi"],
          type: "factory",
          events: ["drawcreate", "drawchange", "drawmove", "drawdelete"],
        },
        // Path:{},
        Livewire: {},
        // Roi:{},
        // FreeHand: {},
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
      file: null,
    };
  },
  methods: {
    onChangeTool: function (tool) {
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      if (tool === "Draw") {
        this.onChangeShape(this.tools.Draw.options[0]);
      }
    },

    // рисование
    onChangeShape: function (shape) {
      if (this.dwvApp && this.selectedTool === "Draw") {
        this.dwvApp.setDrawShape(shape);
      }
    },
    onReset: function () {
      this.dwvApp.resetDisplay();
      this.dwvApp.setTool("Scroll");
      this.toggle_view_flag = true;
      this.toggle_labeling_flag = true;
      this.toggle_labeling = undefined;
      this.toggle_view = undefined;
    },
    setupDropbox() {
      this.showDropbox(true);
    },
    defaultHandleDragEvent: function (event) {
      // prevent default handling
      event.stopPropagation();
      event.preventDefault();
    },
    onBoxDragOver: function (event) {
      this.defaultHandleDragEvent(event);
      // update box border
      const box = document.getElementById(this.dropboxDivId);
      if (box && box.className.indexOf(this.hoverClassName) === -1) {
        box.className += " " + this.hoverClassName;
      }
    },
    onBoxDragLeave: function (event) {
      this.defaultHandleDragEvent(event);
      // update box class
      const box = document.getElementById(this.dropboxDivId);
      if (box && box.className.indexOf(this.hoverClassName) !== -1) {
        box.className = box.className.replace(" " + this.hoverClassName, "");
      }
    },
    onDrop: function (event) {
      this.defaultHandleDragEvent(event);
      // load files
      this.dwvApp.loadFiles(event.dataTransfer.files);
    },
    showDropbox: function (show) {
      const box = document.getElementById(this.dropboxDivId);
      if (!box) {
        return;
      }
      const layerDiv = document.getElementById("layerGroup0");

      if (show) {
        // reset css class
        box.className = this.dropboxClassName + " " + this.borderClassName;
        // check content
        if (box.innerHTML === "") {
          const p = document.createElement("p");
          p.appendChild(document.createTextNode("Drag and drop data here"));
          box.appendChild(p);
        }
        // show box
        box.setAttribute("style", "display:initial");
        // stop layer listening
        if (layerDiv) {
          layerDiv.removeEventListener("dragover", this.defaultHandleDragEvent);
          layerDiv.removeEventListener(
            "dragleave",
            this.defaultHandleDragEvent
          );
          layerDiv.removeEventListener("drop", this.onDrop);
        }
        // listen to box events
        box.addEventListener("dragover", this.onBoxDragOver);
        box.addEventListener("dragleave", this.onBoxDragLeave);
        box.addEventListener("drop", this.onDrop);
      } else {
        // remove border css class
        box.className = this.dropboxClassName;
        // remove content
        box.innerHTML = "";
        // hide box
        box.setAttribute("style", "display:none");
        // stop box listening
        box.removeEventListener("dragover", this.onBoxDragOver);
        box.removeEventListener("dragleave", this.onBoxDragLeave);
        box.removeEventListener("drop", this.onDrop);
        // listen to layer events
        if (layerDiv) {
          layerDiv.addEventListener("dragover", this.defaultHandleDragEvent);
          layerDiv.addEventListener("dragleave", this.defaultHandleDragEvent);
          layerDiv.addEventListener("drop", this.onDrop);
        }
      }
    },
  },
  async mounted() {
    this.file = (
      await http.getItem("File", {
        id: this.$route.params.id,
        showSnackbar: true,
      })
    ).data;
    // create app
    this.dwvApp = new dwv.App();
    // initialise app
    this.dwvApp.init({
      dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
      tools: this.tools,
    });
    // handle load events
    let nLoadItem = null;
    let nReceivedError = null;
    let nReceivedAbort = null;
    let isFirstRender = null;
    this.dwvApp.addEventListener("loadstart", (/*event*/) => {
      // reset flags
      this.dataLoaded = false;
      nLoadItem = 0;
      nReceivedError = 0;
      nReceivedAbort = 0;
      isFirstRender = true;
      // hide drop box
      this.showDropbox(false);
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
        alert("Received errors during load. Check log for details.");
        // show drop box if nothing has been loaded
        if (!nLoadItem) {
          this.showDropbox(true);
        }
      }
      if (nReceivedAbort) {
        this.loadProgress = 0;
        alert("Load was aborted.");
        this.showDropbox(true);
      }
    });
    this.dwvApp.addEventListener("loaditem", (/*event*/) => {
      ++nLoadItem;
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

    // setup drop box
    // this.setupDropbox() // ИЗМЕНЕНО - отключил ручное перетаскивание

    // possible load from location
    dwv.utils.loadFromUri(window.location.href, this.dwvApp);

    this.dwvApp.loadURLs(this.file.paths); // для отладки загрузка из URL
    //TODO загрузка по this.$route.params.id
  },
  computed: {},
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
      if (this.toggle_labeling_flag) {
        this.toggle_labeling_flag = false;
        return;
      }
      console.log("toggle_labeling changed, tool=", shape);

      // нажата кнопка сброса
      if (shape == undefined) {
        // this.dwvApp.setTool('Scroll');
        this.selectedTool = "Scroll";
        return;
      }
      // this.dwvApp.setTool('Draw');
      // this.dwvApp.setDrawShape(shape)

      //деактивация противоположной панели
      this.toggle_view = undefined; //TODO
      this.toggle_view_flag = true;

      if (shape === "Livewire") {
        this.selectedTool = "Livewire";
        this.dwvApp.setTool("Livewire");
        return;
      }

      // активация команды
      console.log("1. before selectedTool");
      this.selectedTool = "Draw";
      this.dwvApp.setTool("Draw");
      console.log("toggle_labeling(), shape = ", shape);
      console.log("3. onChangeShape");
      this.onChangeShape(shape);
    },

    // selectedTool:{
    //   handler(newTool){
    //     this.dwvApp.setTool(newTool);
    //     console.log("2. setTool")
    //   },
    //   immediate: true,
    // },
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
</style>
<!-- non "scoped" style -->
<style>
.layer {
  position: absolute;
  pointer-events: none;
}
</style>