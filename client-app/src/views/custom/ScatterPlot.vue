<template>
    <div id="scatter-plot"> 
    </div>
</template>

<script>
import {APIService} from '../../APIService'
import _ from 'lodash'
const apiService = new APIService();

export default {
  data: function() {
      return {

      }
  },
  props: ['model'],
  methods: {

  },
  watch: { 
            'model': function() {
                console.log("model watched")
                document.getElementById("scatter-plot").innerHTML='';
                Bokeh.embed.embed_item(JSON.parse(this.model.scatter_plot))
            },
        }
}
</script>

<style>
#scatter-plot {

}
</style>