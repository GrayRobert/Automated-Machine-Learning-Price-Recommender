<template>
    <b-card>
        <b-row>
        <b-col>
            <h2>Price Recommendation</h2>
        </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group class="fix-select">
                    <label>Select Previously Trained Model</label>
                    <b-form-select v-model="selectedModelId" :options="modelSelection" class="mb-3" />
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col sm="6">
                <div class="mediumandgrey">Accuracy:</div>
                <div class="bigandgreen">{{ selectedModel.accuracy_r2 | percentageFormatRound }}</div>
            </b-col>
            <b-col sm="6">
                <div class="mediumandgrey">Error: +/-</div>
                <div class="bigandorange"> {{ selectedModel.accuracy_rmse | formatRound }}</div>
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
            <div v-if="results !== null">Price Recommended: {{ results.RecommendedPrice[0] | formatRound}}</div>
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
                    {{ model.id }}
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
    import numeral from 'numeral'

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
            },
            model: {
                type: Object,
                required: false
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
                selectedModel: {},
                models: null,
                formData: {},
                schema: [
                    
                ],
            };
        },
        computed: {
            // Sets the model based on the selected modelId
            findModel: function() {
                const model = _.find(this.models, { 'id': this.selectedModelId }) || ''
                return model
            },
        },
        filters: {
            percentageFormatRound: function(value) {
            return numeral(value).format('0%')
            },
            formatRound: function(value) {
            return numeral(value).format('0.00')
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
                this.selectedModel = model
                const modelArray = JSON.parse(model.test_json)
                this.formData = modelArray[0]
                this.formData.model_id = this.selectedModelId

                // Clear the schema
                this.schema = []

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
                    
                    // Update fields to match model selection
                    this.schema.push(inputField)

                    this.$emit("changeSelectedModelId", this.selectedModelId)
                }


                console.log(this.formData)

            }
        },
        mounted() {
            this.getModelTrainingHistory()
        },
        watch: { 
            'selectedModelId': function() {
                this.parseModel()
            },
            'history': function() {
                this.getModelTrainingHistory()
            },
            'model': function() {
                console.log("model watched")
                this.selectedModelId = this.model.id
            },
        }

    }
</script>

<style>
    div.bigandgreen { 
            color: green; 
            font-family: 'Helvetica Neue', sans-serif; 
            font-size: 8vw; 
            font-weight: bold; 
            letter-spacing: -1px; 
            line-height: 1; 
            padding: 10px 0;
            margin-left:60px;
        }
    div.bigandorange { 
            color: orangered; 
            font-family: 'Helvetica Neue', sans-serif; 
            font-size: 4vw; 
            font-weight: bold; 
            letter-spacing: -1px; 
            line-height: 1; 
            padding: 10px 0;
            margin-left:40px;
        }
    div.mediumandgrey { 
            color: darkslategrey; 
            font-family: 'Helvetica Neue', sans-serif; 
            font-size: 25px; 
            font-weight: bold; 
            letter-spacing: -1px; 
            line-height: 1; 
            vertical-align: top;
            display: inline-block;
            text-align: center;
            margin-left:20px;
        }
</style>