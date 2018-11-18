<template>
  <div class="animated fadeIn">
    <b-row>
      <b-col>
              <TrainModel />
      </b-col>
      <b-col>
        <b-card>
          <b-row>
            <b-col sm="5">
              <h4 id="traffic" class="card-title mb-0">Predicted V Actual</h4>
            </b-col>
            <b-col sm="7" class="d-none d-md-block">
            </b-col>
          </b-row>
          <b-row>
            <img src="/img/charts/predictedvactual.png" height="300" style="margin:auto;"/>
          </b-row>
          <div slot="footer">
            <b-row class="text-center">
                <span>Last Updated: </span>
            </b-row>
          </div>
        </b-card>
      </b-col>
    </b-row>
        <b-row>
      <b-col>
        <PredictModel :history="history"/>
      </b-col>
      <b-col>
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
      </b-col>
    </b-row>
  </div>
</template>

<script>
import TrainModel from './custom/TrainModel'
import PredictModel from './custom/PredictModel'
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
    AtomSpinner
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
      perPage: 8,
      totalRows: 0
    }
  },
  methods: {
      getModelTrainingHistory(){
      apiService.getModelTrainingHistory().then((data) => {
              this.history = data;
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
      }
  },
  mounted () {
    //this.getPrediction()
    this.getModelTrainingHistory()
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
  .predicting-text {
        margin-top:5px;
        color:#20a8d8;
        vertical-align: middle;
        display: inline-block;
    }
</style>
