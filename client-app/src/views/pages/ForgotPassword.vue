<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <b-row class="justify-content-center">
        <b-col md="8">
          <b-card-group>
            <b-card no-body class="p-4">
              <b-card-body>
                <b-form>
                  <h2>Price Recommender</h2>
                  <p class="text-muted">Forgot Password</p>
                  <b-input-group class="mb-3">
                    <b-input-group-prepend><b-input-group-text><i class="icon-user"></i></b-input-group-text></b-input-group-prepend>
                    <b-form-input type="text" class="form-control" placeholder="Email" autocomplete="email" v-model="email" />
                  </b-input-group>
                  <b-row>
                    <b-col>
                      <b-button variant="primary" class="px-4" v-on:click="resetPassword">Reset Password</b-button>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      &nbsp;
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <div class="error" v-for="(error, index) in errors" v-bind:key="index">{{ error }}</div>
                    </b-col>
                  </b-row>
                </b-form>
              </b-card-body>
            </b-card>
          </b-card-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import {APIService} from '../../APIService'
const apiService = new APIService()

export default {  
  name: 'ResetPassword',
  data: function () {
    return {
      email: '',
      showResetFailed: false,
      errors: [],
    }
  },
  methods: {
    resetPassword() {
      // Build up form data
      const formData = new FormData();
      formData.append("email", this.email)

      let self = this;

      // Send Request
      apiService.resetPassword(formData)
        .then((data) => {
          console.log(data)
          self.errors = []
          data.email.forEach(function(error) {
              self.errors.push(error)
          })
        })
    },
  },
  watch: { 

  }
}
</script>

<style>
  .icon-user {
    color:#666;
    margin-bottom: 0px;
  }
  .error {
    color:red;
  }
</style>
