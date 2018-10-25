<template>
  <div class="animated fadeIn">
    <b-row>
      <b-col>
              <FileUpload/>
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
              <h4 id="traffic" class="card-title mb-0">Prediction</h4>
            </b-col>
            <b-col sm="7" class="d-none d-md-block">
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
            <b-row class="text-center">
              <b-col class="col-sm-3">
                <b-button type="submit" size="sm" variant="primary" v-on:click="getPrediction"><i class="fa fa-dot-circle-o"></i> Submit</b-button>
              </b-col>
              <b-col class="col-sm-9">
                <span v-if="results !== null">Predicted Price: {{ results.RecommendedPrice[0] | currency}}</span>
              </b-col>
            </b-row>
          </div>
        </b-card>
      </b-col>
      <b-col>
        <b-card>
          <b-row>
            <b-col sm="5">
              <h4 id="traffic" class="card-title mb-0">Model Training History</h4>
            </b-col>
            <b-col sm="7" class="d-none d-md-block">
            </b-col>
          </b-row>
          <div slot="footer">
            <b-row class="text-center">
            </b-row>
          </div>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import FileUpload from './custom/FileUpload'
import {APIService} from '../APIService'

const apiService = new APIService();

export default {
  name: 'dashboard',
  components: {
    FileUpload
  },
  data: function () {
    return {
      results: null,
      hotel_code: 'TEST1',
      accom_stars: 3,
      staff_pick: 0,
      trip_adv_rating: '3.0',
      has_swimming_pool: 1,
      travel_week: 26,
      booking_week: 26,
    }
  },
  methods: {
    getPrediction(){
      let queryString = 'hotel_code=' + this.hotel_code + '&staff_pick=' + this.staff_pick + '&trip_adv_rating=' + this.trip_adv_rating + '&accom_stars=' + this.accom_stars + '&travel_week=' + this.travel_week + '&booking_week=' + this.booking_week
      console.log('Query String is: ' + queryString)
      apiService.predictPrice(queryString).then((data) => {
              this.results = data;
          })
      },
  },
  mounted () {
    //this.getPrediction()
  }
}
</script>

<style>
  /* IE fix */
  #card-chart-01, #card-chart-02 {
    width: 100% !important;
  }
</style>
