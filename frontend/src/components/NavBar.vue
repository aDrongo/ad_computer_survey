<template>
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <a class="navbar-brand" href="#">
      <img src="https://cdn.nwmsrocks.com/img/3dc41c7.png" alt="Logo" style="width:40px;">
    </a>
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <a class="nav-link" href="#">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" v-on:click='$emit("scan-all")'>Scan</a>
      </li>
      <template v-if="user">
      <li class="nav-item">
        <a class="nav-link"><ModifyDevice v-on:modify-device="modifyDevice"/></a>
      </li>
      <li class="nav-item">
        <a class="nav-link"><Logs /></a>
      </li>
      <li class="nav-item">
        <a class="nav-link"><Users v-on:modify-user="modifyUser"/></a>
      </li>
      </template>
    </ul>
    <a class="navbar-brand"><Login v-on:do-login="login" v-on:do-logout="logout" :user="user" /></a>
  </nav>
</template>

<script>
import ModifyDevice from './ModifyDevice';
import Users from './Users';
import Login from './Login';
import Logs from './Logs';

export default {
  name: 'NavBar',
  components: {
    ModifyDevice,
    Users,
    Login,
    Logs
  },
  props: ["user"],
  methods: {
    modifyDevice(item) {
      this.$emit("modify-device", item)
    },
    modifyUser(form) {
      this.$emit("modify-user", form)
    },
    login(form){
      this.$emit("do-login", form)
    },
    logout(){
      this.$emit("do-logout")
    }
  }
}
</script>

<style scoped>

</style>
