<template>
    <b-card>
        <b-row>
        <b-col sm="5">
            <h1>Test Model Prediction</h1>
        </b-col>
        <b-col sm="7" class="d-none d-md-block">
        </b-col>
        </b-row>
        <b-row>
            <b-col sm="6">
                <b-form>
                    <b-form-group>
                        <b-form-select v-model="selectedModel" :options="modelSelection" class="mb-3" />
                    </b-form-group>
                </b-form>
            </b-col>
        </b-row>
        <b-row>
            <div>Selected: <strong>{{ selectedModel }}</strong></div>
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
</template>

<script>
    import { APIService } from '../../APIService'

    const apiService = new APIService();

    export default {
        components: {
        },
        data: function() {
            return {
                predictingInProgress: false,
                results: null,
                modelSelection: [
                    { value: null, text: 'Please select a model' },
                ],
                selectedModel: null,
            };
        },
        computed: {

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
                let self = this;
                apiService.getModelTrainingHistory().then((data) => {
                    console.log(data)
                    data.forEach(function(model) {
                            self.modelSelection.push(
                                { value: model.id, text: model.id + ' - ' + model.model_type +  ' - ' + model.trained_date}
                            )
                        })
                })    
            },
        },
        mounted() {
            this.getModelTrainingHistory()
        }
    }
</script>

<style>

</style>