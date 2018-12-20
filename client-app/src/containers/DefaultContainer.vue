<template>
  <div class="app">
    <AppHeader fixed class="app-header">
      <SidebarToggler class="d-lg-none" mobile />
      <SidebarToggler class="d-md-down-none" />
      <div class="logo">PR</div>
      <b-navbar-nav class="ml-auto">
        <user-panel/>
      </b-navbar-nav>
    </AppHeader>
    <div class="app-body">
      <main class="main">
        <Breadcrumb :list="list"/>
        <div class="container-fluid">
          <router-view></router-view>
        </div>
      </main>
    </div>
    <TheFooter>
      <!--footer-->
      <div>
        <span class="ml-1">&copy; 2018 Robert Gray.</span>
      </div>
      <div class="ml-auto">
      </div>
    </TheFooter>
  </div>
</template>

<script>
import { Header as AppHeader, SidebarToggler, Sidebar as AppSidebar, SidebarFooter, SidebarForm, SidebarHeader, SidebarMinimizer, SidebarNav, Aside as AppAside, AsideToggler, Footer as TheFooter, Breadcrumb } from '@coreui/vue'
import UserPanel from '../views/custom/UserPanel'

export default {
  name: 'full',
  components: {
    AsideToggler,
    AppHeader,
    AppSidebar,
    AppAside,
    TheFooter,
    Breadcrumb,
    UserPanel,
    SidebarForm,
    SidebarFooter,
    SidebarToggler,
    SidebarHeader,
    SidebarNav,
    SidebarMinimizer
  },
  data () {
    return {
    }
  },
  computed: {
    name () {
      return this.$route.name
    },
    list () {
      return this.$route.matched.filter((route) => route.name || route.meta.label )
    }
  }
}
</script>
<style lang="scss">
  .app-header {
    background-image: linear-gradient(to left, #000000, #29081a, #470135, #5e005c, #68008e, #5d22a7, #4838bf, #004ad7, #0057bd, #00528c, #004759, #003935);
    height:100px;
  }
  .menu-icon {
    color: white !important;
  }
  .fix-select select {
        -moz-appearance:none; /* Firefox */
        -webkit-appearance:none; /* Safari and Chrome */
        appearance:none;
    }
  .logo {
    color: white;
    text-align: center;
    float: left;
    font-size: 2em;
    position: relative;
    top:0px;

  }
</style>