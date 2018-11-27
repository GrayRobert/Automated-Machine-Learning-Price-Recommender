<template>
  <div class="animated fadeIn">
    <b-row>
      <b-col>
        <b-card-group deck>
          <train-model />
          <b-card>
            <b-row>
              <b-col sm="5">
                <h2>Predicted V Actual</h2>
              </b-col>
              <b-col sm="7" class="d-none d-md-block">
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <scatter-plot :model="currentModel" />
              </b-col>
            </b-row>
            <div slot="footer">
              <b-row class="text-center">
                  <span>Based on Model: ID:{{currentModel.id}} | Type:{{currentModel.model_type}}</span>
              </b-row>
            </div>
          </b-card>
        </b-card-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        &nbsp;
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-card-group deck>
          <predict-model :history="history" :model="currentModel" v-on:changeSelectedModelId="changeSelectedModelId($event)"/>
          <b-card header="Model Training History">
            <b-table striped hover responsive="sm" :items="history" :fields="historyFields" :current-page="currentPage" :per-page="perPage">
              <template slot="actions" slot-scope="cell">
                <b-btn size="sm" v-if="cell.item.model_file" @click.stop="deleteModel(cell.item.id)">Delete</b-btn>
              </template>
            </b-table>
            <nav>
              <b-pagination :total-rows="getRowCount(history)" :per-page="perPage" v-model="currentPage" prev-text="Prev" next-text="Next" hide-goto-end-buttons/>
            </nav>
          </b-card>
        </b-card-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        &nbsp;
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <time-series :model="currentModel" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import TrainModel from './custom/TrainModel'
import PredictModel from './custom/PredictModel'
import ScatterPlot from './custom/ScatterPlot'
import TimeSeries from './custom/TimeSeries'
import {APIService} from '../APIService'
import { AtomSpinner } from 'epic-spinners'
import moment from 'moment'
import numeral from 'numeral'

const apiService = new APIService();

export default {
  name: 'dashboard',
  components: {
    TrainModel,
    PredictModel,
    AtomSpinner,
    ScatterPlot,
    TimeSeries
  },
  data: function () {
    return {
      history: [],
      historyFields: [
        {key: 'id'},
        {key: 'model_type'},
        {key: 'dependent_variable'},
        {
          key: 'trained_date',
          formatter: (value) => { return moment(value).format('MMM Do YYYY, h:mm:ss a') }
        },
        {key: 'accuracy_r2',
          formatter: (value) => { return numeral(value).format('0.00%')}},
        {key: 'actions'}
      ],
      currentPage: 1,
      perPage: 5,
      totalRows: 0,
      currentModel: {}
    }
  },
  computed: {

  },
  filters: {
    percentageFormat: function(value) {
      return numeral(value).format('0.00%')
    },
    percentageFormatRound: function(value) {
      return numeral(value).format('0%')
    },
    dateFormat: function(value) {
      return moment(value).format('MMM Do YYYY, h:mm:ss a')
    }
  },
  methods: {
      getModelTrainingHistory(){
      apiService.getModelTrainingHistory().then((data) => {
              this.history = data;
              this.currentModel = _.last(_.orderBy(data, 'accuracy_r2', 'asc')) || ''
          })
      
      },
      getRowCount (items) {
        return items.length
      },
      deleteModel (modelID) {
        console.log('Deleted model: ' + modelID)
        apiService.deleteModel(modelID).then((data) => {
              this.getModelTrainingHistory()
          })
      },
      changeSelectedModelId (modelId) {
        this.currentModel = _.find(this.history, { 'id': modelId })
      }
  },
  mounted () {
    //this.getPrediction()
    this.getModelTrainingHistory()
  },
  watch: { 
            'history': function() {
                console.log('Watched history')
            },
        }
}
</script>

<style>
  /* IE fix */
  #card-chart-01, #card-chart-02 {
    width: 100% !important;
  }
  hr.nice {
    border-top: 1px dotted #8c8b8b;
    border-bottom: 1px dotted #fff;
  }
  h1.nice { 
    color: green; 
    font-family: 'Helvetica Neue', sans-serif; 
    font-size: 175px; 
    font-weight: bold; 
    letter-spacing: -1px; 
    line-height: 1; 
    text-align: center; 
    padding: 50px 0;
    }
  .predicting-text {
        margin-top:5px;
        color:#20a8d8;
        vertical-align: middle;
        display: inline-block;
    }
    .center {
        margin: auto;
        width: 50%;
    }
</style>
