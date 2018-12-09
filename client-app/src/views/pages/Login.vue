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
                  <p class="text-muted">Sign In to your account</p>
                  <b-input-group class="mb-3">
                    <b-input-group-prepend><b-input-group-text><i class="icon-user"></i></b-input-group-text></b-input-group-prepend>
                    <b-form-input type="text" class="form-control" placeholder="Username" autocomplete="username email" v-model="username" />
                  </b-input-group>
                  <b-input-group class="mb-4">
                    <b-input-group-prepend><b-input-group-text><i class="icon-lock"></i></b-input-group-text></b-input-group-prepend>
                    <b-form-input type="password" class="form-control" placeholder="Password" autocomplete="current-password" v-model="password" />
                  </b-input-group>
                  <b-row>
                    <b-col cols="6">
                      <b-button variant="primary" class="px-4" v-on:click="login">Login</b-button>
                    </b-col>
                    <b-col cols="6" class="text-right">
                      
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      &nbsp;
                    </b-col>
                  </b-row>
                  <b-row v-if="showLoginFailed">
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
  name: 'Login',
  data: function () {
    return {
      username: '',
      password: '',
      isAuthenticated: false,
      token: '',
      showLoginFailed: false,
      errors: [],
    }
  },
  methods: {
    login() {
      // Build up form data
      const formData = new FormData();
      formData.append("username", this.username)
      formData.append("password", this.password)

      let self = this;

      // Send Request
      apiService.loginUser(formData)
        .then((data) => {
          console.log(data)
          if(data.key) {
            self.isAuthenticated = true
            self.setCookie(data.key)
          } else {
            self.showLoginFailed = true
            self.errors = []
            data.non_field_errors.forEach(function(error) {
                self.errors.push(error)
            })
          }
        })
    },
    forgotPassword() {

    },
    setCookie(token) {
      const date = new Date
      date.setDate(date.getDate() + 1)
      this.$cookies.set("token",token, date)
      this.$cookies.set("username",this.username, date)
      this.getCookie()
    },
    getCookie() {
      this.token = this.$cookies.get("token")
    },
  },
  watch: { 
    'isAuthenticated': function() {
        if(this.isAuthenticated) {
          this.$router.push('/#/dashboard')
        } 
    },
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
