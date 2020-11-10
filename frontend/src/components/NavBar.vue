<template>
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <a class="navbar-brand" href="#">
      <img src="../assets/logo.png" alt="Logo" style="width:40px;">
    </a>
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <a class="nav-link pointer" href="#">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link pointer" v-on:click='$emit("scan-all")'>Scan</a>
      </li>
      <template v-if="user">
      <li class="nav-item">
        <a class="nav-link pointer"><ModifyDevice v-on:modify-device="modifyDevice" v-on:pause-timer="pauseTimer"/></a>
      </li>
      <li class="nav-item">
        <a class="nav-link pointer"><ModifyUsers v-on:modify-user="modifyUser" v-on:pause-timer="pauseTimer"/></a>
      </li>
      <li class="nav-item">
        <a class="nav-link pointer"><Logs v-on:pause-timer="pauseTimer"/></a>
      </li>
      </template>
    </ul>
    <ul class="navbar-nav">
      <li class="nav-item pointer"><a class="nav-link"><Login v-on:do-login="login" v-on:do-logout="logout" :user="user" v-on:pause-timer="pauseTimer"/></a></li>
    </ul>
  </nav>
</template>

<script>
import ModifyDevice from './ModifyDevice';
import ModifyUsers from './ModifyUsers';
import Login from './Login';
import Logs from './Logs';

export default {
  name: 'NavBar',
  components: {
    ModifyDevice,
    ModifyUsers,
    Login,
    Logs
  },
  props: ["user"],
  methods: {
    pauseTimer(bool){
      this.$emit("pause-timer", bool)
    },
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
