<template>
    <b-card>
          <b-row>
            <b-col>
            <form enctype="multipart/form-data" novalidate v-if="isInitial || isSaving">
                <h1>Upload CSV File</h1>
                <div class="dropbox">
                <input type="file" multiple :name="uploadFieldName" :disabled="isSaving" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"
                    accept="text/csv" class="input-file">
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
                    <li v-for="item in uploadedFiles">
                        <img :src="item.url" class="img-responsive img-thumbnail" :alt="item.originalName">
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
          <div slot="footer">
            <b-row>
                <b-col class="col-sm-3">
                    <b-button type="submit" size="sm" variant="primary" v-on:click="trainModel"><i class="fa fa-dot-circle-o"></i> Train Model</b-button>
                </b-col>
                <b-col class="col-sm-9">
                    <div id="accuracy"><span v-if="accuracy !== null">Accuracy: {{ accuracy.R2 }}</span></div>
                </b-col>
            </b-row>
          </div>
        </b-card>
</template>

<script>
import * as d3 from 'd3';
import {APIService} from '../../APIService'
const apiService = new APIService();

const STATUS_INITIAL = 0, STATUS_SAVING = 1, STATUS_SUCCESS = 2, STATUS_FAILED = 3;

  export default {
    data: function() {
        return {
        uploadedFiles: [],
        accuracy: null,
        uploadError: null,
        currentStatus: null,
        uploadFieldName: 'csv'
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
                .then(x => {
                this.uploadedFiles = [].concat(x);
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
            let queryString = ''
            console.log('Query String is: ' + queryString)
            apiService.trainModel(queryString).then((data) => {
                    this.accuracy = data;
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
        outline: 2px dashed grey; /* the dash box */
        outline-offset: -10px;
        background: lightcyan;
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
        background: lightblue; /* when mouse over to the drop zone, change color */
    }

    .dropbox p {
        font-size: 1.2em;
        text-align: center;
        padding: 50px 0;
    }
</style>