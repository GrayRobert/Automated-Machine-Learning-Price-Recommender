<template slot="dropdown">
    <div>
        <span class="username"> {{ username }} </span>
        <b-dropdown variant="link" size="lg" no-caret>
            <template slot="button-content">
                <i class="fa fa-user fa-lg mr-3 white"></i>
            </template>
            <b-dropdown-header tag="div" class="text-center"><strong>Account</strong></b-dropdown-header>
            <b-dropdown-item><i class="fa fa-user" /> Profile</b-dropdown-item>
            <b-dropdown-item><i class="fa fa-wrench" /> Settings</b-dropdown-item>
            <b-dropdown-item v-on:click="logout"><i class="fa fa-lock" /> Logout</b-dropdown-item>
        </b-dropdown>
    </div>
    
</template>

<script>
import {APIService} from '../../APIService'
const apiService = new APIService()
export default {
  name: 'UserPanel',
  components: {
    
  },
  data: () => {
    return { 
      token: '',
      username: '',
    }
  },
  methods: {
    logout() {
        const formData = new FormData();
        formData.append("username", this.username)
        
        apiService.logoutUser(formData)
        .then((data) => {
            this.$cookies.remove("token")
            this.$cookies.remove("username")
            this.token = ''
            this.$router.push('/pages/login')
        })
    }
  },
  mounted() {
    this.token = this.$cookies.get("token")
    this.username = this.$cookies.get("username")
  }
}
</script>

<style>
    .white {
        color: white;
    }
    .username {
        color: lightgray;
        font-style: oblique;
    }
</style>