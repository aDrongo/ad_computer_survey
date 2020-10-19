<template>
  <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
  <a class="navbar-brand" href="#">
    <img src="https://cdn.nwmsrocks.com/img/3dc41c7.png" alt="Logo" style="width:40px;">
  </a>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="#">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" v-on:click='$emit("scan-all")'>Scan</a>
      </li>
      <li class="nav-item">
        <a class="nav-link"><ModifyDevice v-on:modify-device="modifyDevice"/></a>
      </li>
      <li class="nav-item">
        <a class="nav-link"><Logs /></a>
      </li>
    </ul>
  </nav>
</template>

<script>
import ModifyDevice from './ModifyDevice';
import Logs from './Logs';

export default {
  name: 'NavBar',
  components: {
    ModifyDevice,
    Logs
  },
  methods: {
    modifyDevice(item) {
            this.$emit("modify-device", item)
    }
  }
}
</script>

<style scoped>

</style>
