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
        <v-tabs
          v-model="tab"
          align-with-title
        >
          <v-tabs-slider color="yellow"></v-tabs-slider>

          <v-tab
            v-for="item in tab_items"
            :key="item"
          >
            {{ item }}
          </v-tab>
        </v-tabs>
  
      <v-tabs-items v-model="tab">

        <!-- панель первого генератора на контурах -->
        <v-tab-item>
          <v-card flat class="fill-height d-flex flex-column ma-1">
            <v-card-text>
              <p  class="font-weight-black">Генератор аугментаций №1</p>
              <p class="font-weight-bold">Принцип работы:</p>
              <p class="font-italic">
                1) Генерация случайного гладкого контура неправильной формы;<br/>
                2) Неравномерное сглаживание случайным Гауссовым полем;<br/>
                3) Масштабирование яркости и размера;<br/>
                4) Добавление к исходному изображению;
              </p>
              <p class="font-weight-bold">Особенности:</p>
              <p class="font-italic">
                1) В настоящий момент генерирует только опухоли (новообразования компактной формы);<br>
                2) Работает в полуавтоматическом режиме (требует указания положения и размеров от пользователя);</p>
            </v-card-text>
            <v-spacer vertical></v-spacer>
            <v-row class="ma-1" >
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="x_px"
                  :label="'x, px'"
                  hint="Целое число"
                  persistent-hint
                  prepend-icon="mdi-arrow-right-thin"
                  outlined required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="y_px"
                  :label="'y, px'"
                  hint="Целое число"
                  persistent-hint
                  prepend-icon="mdi-arrow-down-thin"
                  outlined required
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row class="ma-1" >
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="width_px"
                  :label="'Ширина, px'"
                  hint="Целое число"
                  persistent-hint
                  prepend-icon="mdi-arrow-left-right-bold"
                  outlined required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="height_px"
                  :label="'Высота, px'"
                  hint="Целое число"
                  persistent-hint
                  prepend-icon="mdi-arrow-up-down-bold"
                  outlined required
                ></v-text-field>
              </v-col>
            </v-row>
            
            <!-- :rules="[rules.required, rules.date]"
                :readonly="all_readonly" -->

            <v-row class="ma-1" >
              <v-btn
                class="ma-1"
                color="primary"
                :loading="loading"
                @click="onGenerate">
                Генерация
              </v-btn>
              <v-btn class="ma-1" outlined @click="onSave">
                <v-icon>mdi-content-save</v-icon>
                Сохранить
              </v-btn>
              <v-btn class="ma-1" color="error" outlined @click="onCancel">
                Выход
              </v-btn>
            </v-row>
          </v-card>
        </v-tab-item>

        <!-- панель второго генератора на ML -->
        <v-tab-item>
          <v-card flat  class="fill-height d-flex flex-column ma-1">
            <v-card-text>
              <p  class="font-weight-black">Генератор аугментаций №1</p>
              <p class="font-weight-bold">Принцип работы:</p>
              <p class="font-italic">
                1) ...;<br/>
                2) ...;<br/>
                3) ...;<br/>
                4) .;
              </p>
              <p class="font-weight-bold">Особенности:</p>
              <p class="font-italic">
                1) ...;<br>
                2) ...;</p>
            </v-card-text>
            <v-spacer vertical></v-spacer>
            <v-row class="ma-1" >
              <v-btn
                class="ma-1"
                color="primary"
                :loading="loading"
                @click="onGenerate2">
                Генерация
              </v-btn>
              <v-btn class="ma-1" outlined @click="onSave2">
                <v-icon>mdi-content-save</v-icon>
                Сохранить
              </v-btn>
              <v-btn class="ma-1" color="error" outlined @click="onCancel2">
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

<!-- <script type="text/javascript" src="../components/dwv-jqui/src/gui/infoController.js"></script>
<script type="text/javascript" src="../components/dwv-jqui/src/gui/infoOverlay.js"></script> -->
<script>
// import http from "@/http"; //XXX  раскомментировать для перекладки страницы с тестовых данных на работу с сервом
// import dwvVue from 'dwv';
// import dwvVue from '../components/dwv';

import Vue from "vue";
// import MdButton from "vue-material";
import dwv from "dwv";
// import dwvjq.gui.info.Controller from '../components/dwv-jqui/src/gui/infoController.js'
// import {InfoController} from '../components/dwv-jqui/src/gui/infoController_copy.js'
// import {dwvjq} from '../components/dwv-jqui/src/gui/infoOverlay.js'
// import {dwvjq, startDwvjq} from '../components/dwv-jqui/src/dwv_jquiexport.js'

// Vue.use(MdButton);

// gui overrides

// Image decoders (for web workers)
dwv.image.decoderScripts = {
  jpeg2000: "assets/dwv/decoders/pdfjs/decode-jpeg2000.js",
  "jpeg-lossless": "assets/dwv/decoders/rii-mango/decode-jpegloss.js",
  "jpeg-baseline": "assets/dwv/decoders/pdfjs/decode-jpegbaseline.js",
  rle: "assets/dwv/decoders/dwv/decode-rle.js",
};

// dwv.tool = {};

// dwv.tool.colourMaps = {
//     plain: dwv.image.lut.plain,
//     invplain: dwv.image.lut.invPlain,
//     rainbow: dwv.image.lut.rainbow,
//     hot: dwv.image.lut.hot,
//     hotiron: dwv.image.lut.hot_iron,
//     pet: dwv.image.lut.pet,
//     hotmetalblue: dwv.image.lut.hot_metal_blue,
//     pet20step: dwv.image.lut.pet_20step
//   };

dwv.tool.defaultpresets = {};

dwv.tool.defaultpresets.CT = {
    mediastinum: {center: 40, width: 400},
    lung: {center: -500, width: 1500},
    bone: {center: 500, width: 2000},
    brain: {center: 40, width: 80},
    head: {center: 90, width: 350}
  };

export default {
  name: "ViewGeneration",
  components: {
    // dwvVue,
    // tagsTable,
    // Controller,
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

      dwvApp: null, // библиотека DWV
      infoController: null, // оверлей с информацией о снимке
      infoControllerVisible : false, // состояние оверлея с информацией
      // standardWindows : ["Window1", "Window2", "Lung"],
      selectedStndardWindow : null,
      layergroup : null,
      viewController : null,
      presetNames : null, // пресеты по уровням яркости
      drawColor : '#FF0000',

      isSelecting: false, // для загрузки разметки в json
      selectedFile: null, // файл для загрузки разметки в json
      
      annotations:{
        objects:[
          {x:1,y:2},
        ]}, // объекты разметки для перевода в JSON
      tab : null,
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

      x_px : 150,
      y_px : 250,
      width_px : 30,
      height_px : 30,

      loading: true,

    };
  },
  methods: {
    // Группа методов для первого алгоритма генерации (моего)

    onGenerate(){
      // TODO отправка запроса на генерацию с параметрами
      //    this.x_px
      //    this.y_px
      //    this.width_px
      //    this.height_px

      // ожидание получения  результата
      this.loading=true;

      // TODO ожидание

      // TODO в конце ожидания (может надо куда-то перенести)
      // загрузка результата генерации из URL:
      this.dwvApp.reset();
      this.dwvApp.init({
        dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
        tools: this.tools,
      });
      this.dwvApp.loadURLs(["1-14.dcm", "1-15.dcm", "1-16.dcm"]);

      // завершение индикатора ожидания
      // в this.dwvApp.addEventListener("loadend"... ниже
      // ... я уже прописал
    },

    onSave(){
      //TODO выход с сохранением
    },

    onCancel(){
      //TODO возврат без сохранения
    },

    // Группа методов для второго алгоритма

    onGenerate2(){
      // TODO отправка запроса на генерацию с параметрами
      //    this.x_px
      //    this.y_px
      //    this.width_px
      //    this.height_px

      // ожидание получения  результата
      this.loading=true;

      // TODO ожидание

      // TODO в конце ожидания (может надо куда-то перенести)
      // загрузка результата генерации из URL:
      this.dwvApp.reset();
      this.dwvApp.init({
        dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
        tools: this.tools,
      });
      this.dwvApp.loadURLs(["1-14.dcm", "1-15.dcm", "1-16.dcm"]);

      // завершение индикатора ожидания
      // в this.dwvApp.addEventListener("loadend"... ниже
      // ... я уже прописал
    },

    onSave2(){
      //TODO выход с сохранением
    },

    onCancel2(){
      //TODO возврат без сохранения
    },

    onChangeTool: function (tool) { // при выборе инструмента разметки
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      this.dwvApp.setDrawLineColour(this.drawColor);
      if (tool === "Draw") {
        this.onChangeShape(this.tools.Draw.options[0]);
        this.dwvApp.setDrawLineColour(this.drawColor); // работает на выбранном инструменте
      }
    },

    // рисование
    onChangeShape: function (shape) { 
      if (this.dwvApp && this.selectedTool === "Draw") {
        this.dwvApp.setDrawShape(shape);
        this.dwvApp.setDrawLineColour(this.drawColor);
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

    onContoursSave(){
      this.annotations = this.dwvApp.getState();
      console.log("onContoursSave(): getState = ", this.annotations);
      
      // this.annotations = this.dwvApp.getDrawDisplayDetails();
      // console.log("onContoursSave(): getDrawDisplayDetails = ", this.annotations);
      
      // var y = this.dwvApp.getDrawStoreDetails();
      // console.log("onContoursSave(): getDrawStoreDetails = ", y);
      // var json = state.toJSON(app);

      // XXX TODO сохранение JSON-разметки this.annotations в БД
    },

    onSetPreset(presetname){
      this.dwvApp.setWindowLevelPreset(presetname);
    },

    onDownloadJsonClicked(){ // закачка файла с разметкой
      this.saveTemplateAsFile("annotations.json", this.annotations);
    },

    saveTemplateAsFile(filename, dataObjToWrite) {
      // const blob = new Blob([JSON.stringify(dataObjToWrite)], {
      const blob = new Blob([dataObjToWrite], {
        type: "text/json",
      });
      const link = document.createElement("a");

      link.download = filename;
      link.href = window.URL.createObjectURL(blob);
      link.dataset.downloadurl = ["text/json", link.download, link.href].join(
        ":"
      );

      const evt = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
      });

      link.dispatchEvent(evt);
      link.remove();
    },

    handleFileImport() {
      this.isSelecting = true;

      // After obtaining the focus when closing the FilePicker, return the button state to normal
      window.addEventListener('focus', () => {
          this.isSelecting = false
      }, { once: true });
      
      // Trigger click on the FileInput
      this.$refs.uploader.click();
    },

    onFileChanged(e) {
      // функция вызывается, когда файл JSON загружается на страницу
      // для восстановления разметки

      this.selectedFile = e.target.files[0];
      
      // Do whatever you need with the file, liek reading it with FileReader
      const file= e.target.files[0];
      console.log("selectedFile = ", file);

      let reader = new FileReader();
      reader.onload = (e) => {
          this.selectedFile = e.target.result;
          // This is a regular expression to identify carriage
          // Returns and line breaks
          // this.selectedFile = file_contents.split(/\r\n|\n/);
          console.log("split = ", this.selectedFile);
          console.log("typeof split = ", typeof(this.selectedFile));
          var state = new dwv.io.State();
          console.log("state = ", state);
          // https://github.com/ivmartel/dwv/blob/develop/tests/state/state.test.js
          var jsonData = state.fromJSON(e.target.result);
          console.log("fromJSON = ", jsonData);
          state.apply(this.dwvApp, jsonData);
      };
      reader.onerror = (e) => alert(e.target.error.name);
      reader.readAsText(file);
    },
  },

  mounted() {
    // create app
    this.dwvApp = new dwv.App();
    console.log("mounted(): this.dwvApp = ", this.dwvApp);

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
    this.dwvApp.addEventListener("loadstart", (event) => {
      // reset flags
      this.dataLoaded = false;
      nLoadItem = 0;
      nReceivedError = 0;
      nReceivedAbort = 0;
      isFirstRender = true;
      // hide drop box
      this.showDropbox(false);
      if (event.loadtype === "image") {
        // this.infoController.onLoadStart();
      }
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
          // this.showDropbox(true);
        }
      }
      if (nReceivedAbort) {
        this.loadProgress = 0;
        alert("Load was aborted.");
        // this.showDropbox(true);
      }

      this.loading=false;

      this.layergroup = 
          this.dwvApp.getActiveLayerGroup();
        this.viewController =
          this.layergroup.getActiveViewLayer().getViewController();
        this.presetNames =
          this.viewController.getWindowLevelPresetsNames()


        console.log("layer group = ", this.layergroup);
        console.log("viewController = ", this.viewController);
        console.log("presetNames = ", this.presetNames);
        
        // dwv.setDrawLineColour('Red');
        // console.log("layer group = ", this.dwvApp.getActiveLayerGroup());

    });
    this.dwvApp.addEventListener("loaditem", (event) => {
      ++nLoadItem;
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

    // setup drop box
    // this.setupDropbox() // ИЗМЕНЕНО - отключил ручное перетаскивание

    // possible load from location
    dwv.utils.loadFromUri(window.location.href, this.dwvApp);
    console.log("dwv = ", dwv);
    console.log("dwvApp = ", this.dwvApp);
    // this.dwvApp.loadURLs([this.file.path]); //XXX для отладки загрузка из URL
    this.dwvApp.loadURLs(["Malignant case (1).jpg"]);

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

    toggle_labeling: function (shape) { // при выборе инструмента разметки

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
        this.dwvApp.setDrawLineColour(this.drawColor);
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