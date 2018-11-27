<template>
    <b-card header="Model Prediction Time Series">
        
    </b-card>
</template>

<script>
import {APIService} from '../../APIService'
import _ from 'lodash'
const apiService = new APIService();
import moment from 'moment'

export default {
    data: function() {
        return {

        }
    },
    props: ['model'],
    methods: {
        getWeeks() {
            const start = moment('2018-01-01'),
                end   = moment('2018-12-30'),
                day   = 6; // Saturday

            let result = [];
            let current = start.clone();

            while (current.day(7 + day).isBefore(end)) {
            result.push(current.clone());
            }

            console.log(result.map(m => m.format('YYYY-MM-DD')));
        }
    },
    watch: { 
        'model': function() {
        console.log("model watched")
        },
    },
    mounted() {
        this.getWeeks()
    }

}
</script>

<style>

</style>