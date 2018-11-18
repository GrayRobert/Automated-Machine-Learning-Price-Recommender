<template>
  <div>
    <component v-for="(field, index) in schema"
               :key="index"
               :is="field.fieldType"
               :value="formData[field.name]"
               @input="updateForm(field.name, $event)"
               v-bind="field">
    </component>
  </div>
</template>

<script>
import NumberInput from "./NumberInput";
import TextInput from "./TextInput";
export default {
  name: "FormGenerator",
  components: { NumberInput, TextInput },
  props: ["schema", "value"],
  data() {
    return {
      formData: this.value || {}
    };
  },
  methods: {
    updateForm(fieldName, value) {
        this.$nextTick(function () {
            this.$set(this.formData, fieldName, value);
            this.$emit("input", this.formData);
        })

    }
  },
  watch: {
    // we need to watch for the value props being set when user selects model to predict with
    value: function () {
      this.formData= this.value
    }
  },
};
</script>
