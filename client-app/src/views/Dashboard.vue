<template>
  <div class="animated fadeIn">
    <b-row>
      <b-col>
              <TrainModel/>
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
        <b-card>
          <b-row>
            <b-col sm="5">
              <h1>Test Model Prediction</h1>
            </b-col>
            <b-col sm="7" class="d-none d-md-block">
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Select Machine Learning Model"
                label-for="model_select_predict"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="model_select_predict"
                  :plain="true"
                  :options="[
                    {text: 'Random Forrest ',value: 'RFR'},
                    {text: 'Xtra Trees ',value: 'EXT'},
                  ]"
                  :checked="2" v-model="model_select_predict">
                </b-form-radio-group>
              </b-form-group>
              <hr class="nice" />
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group>
                <label for="hotel_code">Hotel Code</label>
                <b-form-input type="text" id="name_code" placeholder="TEST1" v-model="hotel_code"></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Staff Pick"
                label-for="staff_pick"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="staff_pick"
                  :plain="true"
                  :options="[
                    {text: 'Yes ',value: '1'},
                    {text: 'No ',value: '0'},
                  ]"
                  :checked="2" v-model="staff_pick">
                </b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Accommodation Star Rating"
                label-for="accom_stars"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="accom_stars"
                  :plain="true"
                  :options="[
                    {text: '1 ',value: '1'},
                    {text: '2 ',value: '2'},
                    {text: '3 ',value: '3'},
                    {text: '4 ',value: '4'},
                    {text: '5 ',value: '5'},
                  ]"
                  :checked="3" v-model="accom_stars">
                </b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Trip Advisor Rating"
                label-for="trip_adv_rating"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="trip_adv_rating"
                  :plain="true"
                  :options="[
                    {text: '0.5 ' ,value: '0.5'},
                    {text: '1.0 ',value: '1.0'},
                    {text: '1.5 ' ,value: '1.5'},
                    {text: '2.0 ',value: '2.0'},
                    {text: '2.5 ' ,value: '2.5'},
                    {text: '3.0 ',value: '3.0'},
                    {text: '3.5 ' ,value: '3.5'},
                    {text: '4.0 ',value: '4.0'},
                    {text: '4.5 ' ,value: '4.5'},
                    {text: '5.0 ',value: '5.0'},
                  ]"
                  :checked="3.0" v-model="trip_adv_rating">
                </b-form-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Swimming Pool"
                label-for="has_swimming_pool"
                :label-cols="10"
                :horizontal="false">
                <b-form-radio-group id="has_swimming_pool"
                  :plain="true"
                  :options="[
                    {text: 'Yes ',value: '1'},
                    {text: 'No ',value: '0'},
                  ]"
                  :checked="2" v-model="has_swimming_pool">
                </b-form-radio-group>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <label for="travel_week">Travel Week #/52</label>
                <b-form-input type="text" id="travel_week" placeholder="26" v-model="travel_week"></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <label for="booking_week">Booking Week #/52</label>
                <b-form-input type="text" id="booking_week" placeholder="26" v-model="booking_week"></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <div slot="footer">
            <b-row>
              <b-col class="col-sm-3">
                <b-button type="submit" size="sm" variant="primary" v-on:click="getPrediction"><i class="fa fa-dot-circle-o"></i> Predict Price</b-button>
              </b-col>
              <b-col class="col-sm-9">
                <b-row v-if="predictingInProgress">
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
                        <span class="predicting-text">Predicting in progress...</span>
                    </b-col>
                </b-row>
                <div v-if="results !== null">Predicted Price: {{ results.RecommendedPrice[0] | currency}}</div>
              </b-col>
            </b-row>
          </div>
        </b-card>
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
import {APIService} from '../APIService'
import { AtomSpinner } from 'epic-spinners'
import moment from 'moment'
import numeral from 'numeral'

const apiService = new APIService();

export default {
  name: 'dashboard',
  components: {
    TrainModel,
    AtomSpinner
  },
  data: function () {
    return {
      results: null,
      model_select_predict: 'RFR',
      hotel_code: 'TEST1',
      accom_stars: 3,
      staff_pick: 0,
      trip_adv_rating: '3.0',
      has_swimming_pool: 1,
      travel_week: 26,
      booking_week: 26,
      predictingInProgress: false,
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
    getPrediction(){
      this.predictingInProgress = true
      let queryString = 'hotel_code=' + this.hotel_code + '&staff_pick=' + this.staff_pick + '&has_swimming_pool=' + this.has_swimming_pool + '&trip_adv_rating=' + this.trip_adv_rating + '&accom_stars=' + this.accom_stars + '&travel_week=' + this.travel_week + '&booking_week=' + this.booking_week + '&model_type=' + this.model_select_predict
      console.log('Query String is: ' + queryString)
      apiService.predictPrice(queryString).then((data) => {
              this.results = data;
              this.predictingInProgress = false
          })
      
      },
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
