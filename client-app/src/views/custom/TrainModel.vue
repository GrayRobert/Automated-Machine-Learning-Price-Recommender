<template>
    <b-card>
          <b-row>
            <b-col>
            <form enctype="multipart/form-data" novalidate>
                <h1 v-if="isInitial || isSaving">Upload CSV File</h1>
                <h1 v-if="isSuccess">Uploaded {{ uploadedFiles.length }} file(s) successfully.</h1>
                <div class="dropbox">
                <input type="file" :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
                    accept="text/csv" class="input-file">
                    <div v-if="isInitial">
                        <div class="arrow-down"></div>
                        <p>Drop your CSV file here <br> or click to browse</p>
                    </div>
                    <p v-if="isSaving">
                    Uploading {{ fileCount }} files...
                    </p>
                    <div v-if="isSuccess">
                        <ul class="list-unstyled">
                        <li v-for="file in uploadedFiles">
                            {{ file }}
                        </li>
                        </ul>
                    </div>
                    <div v-if="isFailed">
                        <h2>Uploaded failed.</h2>
                        <p>
                        <a href="javascript:void(0)" @click="reset()">Try again</a>
                        </p>
                        <pre>{{ uploadError }}</pre>
                    </div>
                </div>
            </form>
            </b-col>
          </b-row>
          <div slot="footer">
            <b-row>
                <b-col class="col-sm-2">
                    <b-button type="submit" size="sm" variant="primary" v-on:click="preProcessModal = true"><i class="fa fa-dot-circle-o"></i> Train Model</b-button>
                </b-col>
                <b-col class="col-sm-10">
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
            <b-modal title="Model Training Options" size="lg" v-model="preProcessModal" @ok="preProcessModal = false" ok-title="Train">
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Select categroical fields to encode"
                            label-for="encodeCatFields"
                            :label-cols="3"
                            :horizontal="true">
                            <b-form-select id="encodeCatFields"
                                :plain="true"
                                :multiple="true"
                                :options="fieldOptions"
                                v-model="encodeCatFields">
                                </b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Select date fields to encode"
                            label-for="encodeDateFields"
                            :label-cols="3"
                            :horizontal="true">
                            <b-form-select id="encodeDateFields"
                                :plain="true"
                                :multiple="true"
                                :options="fieldOptions"
                                v-model="encodeDateFields">
                                </b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Select fields to drop (Excluding Target)"
                            label-for="dropFields"
                            :label-cols="3"
                            :horizontal="true">
                            <b-form-select id="dropFields"
                                :plain="true"
                                :multiple="true"
                                :options="fieldOptions"
                                v-model="dropFields">
                                </b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Select field to predict"
                            label-for="predictField"
                            :label-cols="3"
                            :horizontal="true">
                            <b-form-select id="predictField"
                            :plain="true"
                            :options="fieldOptions"
                            value="Please select"
                            v-model="predictField">
                            </b-form-select>
                        </b-form-group>
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
                <b-row>
                    <b-col>
                        Encode Categorical Fields: {{ encodeCatFields }}
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        Encode Date Fields: {{ encodeDateFields }}
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        Drop Fields: {{ dropFields }}
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        Predict Field: {{ predictField }}
                    </b-col>
                </b-row>
                <div slot="modal-footer">
                    <b-button type="submit" size="sm" variant="primary" v-on:click="trainModel"><i class="fa fa-dot-circle-o"></i> Train Model</b-button>
                </div>
            </b-modal>
        </b-card>
</template>

<script>
import * as d3 from 'd3';
import { APIService } from '../../APIService'
import { AtomSpinner } from 'epic-spinners'
import Papa from 'papaparse'

const apiService = new APIService()
const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {
    components: {
      AtomSpinner
    },
    data: function() {
        return {
            preProcessModal: false,
            uploadedFiles: [],
            accuracy: null,
            uploadError: null,
            currentStatus: null,
            uploadFieldName: 'file',
            trainingInProgress: false,
            model_select_train: 'RFR',
            modelFields: [],
            fieldOptions: [],
            encodeCatFields: [],
            encodeDateFields: [],
            dropFields: [],
            predictField: null,
            categroicals: [],
            targetVariable: null
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
            let self = this;

            const papaConfig = {
                    header: true,
                    dynamicTyping: true,
                    preview: 10,
                    complete: function (data) {
                        self.modelFields = data.meta.fields
                        self.modelFields.forEach(function(field) {
                            self.fieldOptions.push({
                                text: field,
                                value: field
                            })
                        })
                    },
                    error: function (err) {
                        console.log(err);
                    }
                }


            Papa.parse(fileList[0], papaConfig);

            if (!fileList.length) return;

            // append the files to FormData
            formData.append(fieldName, fileList[0], fileList[0].name);


            

            // save it
            this.save(formData);
        },
        trainModel(){
            // Update our view
            this.preProcessModal = false
            this.trainingInProgress = true
            
            // Remove value to predict
            let modelFields = this.modelFields
            modelFields.splice( modelFields.indexOf(this.predictField), 1 );

            // Build up our model training payload
            const formData = new FormData();
            formData.append("encodecat", this.encodeCatFields)
            formData.append("encodedate", this.encodeDateFields)
            formData.append("drop", this.dropFields)
            formData.append("predict", this.predictField)
            formData.append("model", this.model_select_train)
            formData.append("variables", modelFields)

            // Send Request
            apiService.trainModel(formData).then((data) => {
                    this.accuracy = data
                    this.trainingInProgress = false
                    this.$parent.getModelTrainingHistory();
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