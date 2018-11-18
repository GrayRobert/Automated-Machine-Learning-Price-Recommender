<template>
  <b-row>
    <b-col class="form-group">
        <label for="name">{{label}}</label>
        <input 
          type="text"
          :name="name"
          :value="placeholder"
          @input="$emit('input',$event.target.value)"
          :placeholder="placeholder" 
          class="form-control"
        />
    </b-col>
  </b-row>
</template>
<script>
export default {
  name: 'TextInput',
  props: ['placeholder', 'label', 'name', 'value']
}
</script>