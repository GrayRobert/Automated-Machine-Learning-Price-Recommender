<template>
    <b-card>
          <b-row>
            <b-col>
            <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
                <h1>Upload CSV File</h1>
                <div class="dropbox">
                <input type="file" :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
                    accept="text/csv" class="input-file">
                    <div class="arrow-down"></div>
                    <p v-if="isInitial">
                    Drop your file(s) here <br> or click to browse
                    </p>
                    <p v-if="isSaving">
                    Uploading {{ fileCount }} files...
                    </p>
                </div>
            </form>
            </b-col>
          </b-row>
          <b-row>
              <b-col>
                  <div v-if="isSuccess">
                    <h2>Uploaded {{ uploadedFiles.length }} file(s) successfully.</h2>
                    <p>
                    <a href="javascript:void(0)" @click="reset()">Upload again</a>
                    </p>
                    <ul class="list-unstyled">
                    <li v-for="file in uploadedFiles">
                        {{ file }}
                    </li>
                    </ul>
                </div>
                <!--FAILED-->
                <div v-if="isFailed">
                    <h2>Uploaded failed.</h2>
                    <p>
                    <a href="javascript:void(0)" @click="reset()">Try again</a>
                    </p>
                    <pre>{{ uploadError }}</pre>
                </div>
              </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Select Machine Learning Model"
                label-for="model_select_train"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="model_select_train"
                  :plain="true"
                  :options="[
                    {text: 'Random Forrest ',value: 'RFR'},
                    {text: 'Xtra Trees ',value: 'EXT'},
                  ]"
                  :checked="2" v-model="model_select_train">
                </b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <div slot="footer">
            <b-row>
                <b-col class="col-sm-3">
                    <b-button type="submit" size="sm" variant="primary" v-on:click="trainModel"><i class="fa fa-dot-circle-o"></i> Train Model</b-button>
                </b-col>
                <b-col class="col-sm-9">
                    <b-row v-if="trainingInProgress">
                        <b-col class="col-sm-2">
                            <div>
                                <atom-spinner
                                :animation-duration="1000"
                                :size="30"
                                color="#20a8d8"
                                />
                            </div>
                        </b-col>
                        <b-col class="col-sm-10">
                            <span class="training-text">Training in progress...</span>
                        </b-col>
                    </b-row>
                    <div id="accuracy"><span v-if="accuracy !== null">Accuracy: {{ accuracy.R2 }}</span></div>
                </b-col>
            </b-row>
          </div>
        </b-card>
</template>

<script>
import * as d3 from 'd3';
import {APIService} from '../../APIService'
import { AtomSpinner } from 'epic-spinners'

const apiService = new APIService()


const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {
    components: {
      AtomSpinner
    },
    data: function() {
        return {
        uploadedFiles: [],
        accuracy: null,
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'file',
        trainingInProgress: false,
        model_select_train: 'RFR',
        };
    },
    computed: {
      isInitial() {
        return this.currentStatus === STATUS_INITIAL;
      },
      isSaving() {
        return this.currentStatus === STATUS_SAVING;
      },
      isSuccess() {
        return this.currentStatus === STATUS_SUCCESS;
      },
      isFailed() {
        return this.currentStatus === STATUS_FAILED;
      }
    },
    methods: {
        reset() {
            // reset form to initial state
            this.currentStatus = STATUS_INITIAL;
            this.uploadedFiles = [];
            this.uploadError = null;
        },
        save(formData) {
        // upload data to the server
        this.currentStatus = STATUS_SAVING;

            apiService.uploadFile(formData)
                .then(response => {
                this.uploadedFiles = [].concat(response.FileName);
                this.currentStatus = STATUS_SUCCESS;
                })
                .catch(err => {
                this.uploadError = err.response;
                this.currentStatus = STATUS_FAILED;
                });
            },
            filesChange(fieldName, fileList) {
            // handle file changes
            const formData = new FormData();

            if (!fileList.length) return;

            // append the files to FormData
            Array
                .from(Array(fileList.length).keys())
                .map(x => {
                formData.append(fieldName, fileList[x], fileList[x].name);
                });

            // save it
            this.save(formData);
        },
        trainModel(){
            this.trainingInProgress = true
            let queryString = 'model_type=' + this.model_select_train
            console.log('Query String is: ' + queryString)
            apiService.trainModel(queryString).then((data) => {
                    this.accuracy = data
                    this.trainingInProgress = false
                })
        },
    },
    mounted() {
        this.reset();
    }
  }
</script>

<style>
    .dropbox {
        border: 20px;
        border-top: 0;
        border-style: solid;
        border-color: rgb(243, 241, 241);
        margin:30px;
        background: rgba(255, 255, 255, 0.705);
        color: dimgray;
        padding: 10px 10px;
        min-height: 200px; /* minimum height */
        position: relative;
        cursor: pointer;
    }

    .input-file {
        opacity: 0; /* invisible but it's there! */
        width: 100%;
        height: 200px;
        position: absolute;
        cursor: pointer;
    }

    .dropbox:hover {
        background: rgba(235, 235, 235, 0.562); /* when mouse over to the drop zone, change color */
    }

    .dropbox p {
        font-size: 1.2em;
        text-align: center;
        padding: 50px 0;
    }

    .arrow-down {
        width: 0; 
        height: 0;
        left: 45%;
        top:20%;
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;

        border-top: 20px solid rgb(231, 231, 231);
        position: absolute;
    }
    .training-text {
        margin-top:5px;
        color:#20a8d8;
        vertical-align: middle;
        display: inline-block;
    }
</style>