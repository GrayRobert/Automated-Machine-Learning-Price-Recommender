<template>
    <b-card>
        <b-row>
        <b-col>
            <h1>Price Recommendation</h1>
        </b-col>
        </b-row>
        <b-row>
            <b-col sm="6">
                <b-form-group>
                    <label>Select Previously Trained Model</label>
                    <b-form-select v-model="selectedModelId" :options="modelSelection" class="mb-3" />
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                
            </b-col>
        </b-row>
        <div slot="footer">
        <b-row>
            <b-col class="col-sm-3">
                <b-button type="submit" size="sm" variant="primary" v-on:click="preProcessModal = true"><i class="fa fa-dot-circle-o"></i> Get Recommendation</b-button>
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
                    <span class="predicting-text">Recommending in progress...</span>
                </b-col>
            </b-row>
            <div v-if="results !== null">Price Recommended: {{ results.RecommendedPrice[0] | currency}}</div>
            </b-col>
        </b-row>
        </div>
        <b-modal title="Price Recommendation Options" size="lg" v-model="preProcessModal" @ok="preProcessModal = false" ok-title="Recommend Price">
            <b-row>
                <b-col>
                    <form-generator 
                        :schema="schema"
                        v-model="formData">
                    </form-generator>
                </b-col>
                {{ formData }}
            </b-row>
            <div slot="modal-footer">
                    <b-button type="submit" size="sm" variant="primary" v-on:click="getPrediction"><i class="fa fa-dot-circle-o"></i> Recommend Price</b-button>
                </div>
        </b-modal>
    </b-card>
</template>

<script>
    import { APIService } from '../../APIService'
    import { AtomSpinner } from 'epic-spinners'
    import moment from 'moment'
    import _ from 'lodash'
    import FormGenerator from './FormGenerator'

    import JQuery from 'jquery'
    let $ = JQuery

    const apiService = new APIService();

    export default {
        name: "PredictModel",
        components: {
            FormGenerator,
            AtomSpinner
        },
        props: { 
            history: {
                type: Array,
                required: true
            }
        },
        data: function() {
            return {
                preProcessModal: false,
                predictingInProgress: false,
                results: null,
                modelSelection: [
                    { value: null, text: 'Please select a model' },
                ],
                selectedModelId: null,
                models: null,
                formData: {},
                schema: [
                    
                ]
            };
        },
        computed: {
            // Sets the model based on the selected modelId
            findModel: function() {
                const model = _.find(this.models, { 'id': this.selectedModelId }) || ''
                return model
            },
        },
        methods: {
            getPrediction(){
                this.preProcessModal = false
                this.predictingInProgress = true
                let queryString = $.param(this.formData); // This bit of JQuery turns the form data into a query string
                console.log('Query String is: ' + queryString)
                apiService.predictPrice(queryString).then((data) => {
                        this.results = data;
                        this.predictingInProgress = false
                    })
            },
            getModelTrainingHistory(){
                let self = this;
                // Add any models that have a model_file
                self.modelSelection = []
                this.history.forEach(function(model) {
                    if(model.model_file) {
                        self.modelSelection.push(
                            { value: model.id, text: model.id + ' - ' + model.model_type +  ' - ' + self.formatDate(model.trained_date)}
                        )
                    }
                })  
            },
            formatDate(date){
                return moment(date).format('MMM Do YYYY, h:mm:ss a')
            },
            parseModel(){
                const model = _.find(this.history, { 'id': this.selectedModelId })
                const modelArray = JSON.parse(model.test_json)
                this.formData = modelArray[0]
                this.formData.model_id = this.selectedModelId

                for (const [key, value] of Object.entries(this.formData)) {
                    
                    //don't need a for field for this
                    if (key === 'model_id') { continue; }

                    let inputField = {}
                    if(isNaN(value)){
                        inputField = {
                        fieldType: "TextInput",
                        placeholder: value.toString(),
                        value: value.toString(),
                        label: key,
                        name: key
                        }
                    } else {
                        inputField = {
                        fieldType: "NumberInput",
                        placeholder: parseInt(value, 10),
                        value: parseInt(value, 10),
                        label: key,
                        name: key
                        }
                    }
                    
                    this.schema.push(inputField)
                }


                console.log(this.formData)

            }
        },
        mounted() {
            this.getModelTrainingHistory()
        },
        watch: { 
            'selectedModelId': function() {
                console.log('Watched selectedModelId')
                this.parseModel()
            },
            'history': function() {
                console.log('Watched history')
                this.getModelTrainingHistory()
            }
        }

    }
</script>

<style>

</style>