<template>
  <div class="Location m-1" :id="location">
    <h2>{{location}}</h2>
    <Devices v-bind:devices="devices" v-bind:location="location" v-on:scan-device="emitScanDevice" />
  </div>
</template>

<script>
import Devices from './Devices';

export default {
  name: 'Location',
  components: {
    Devices
  },
  props: ["devices","location"],
  methods: {
    emitScanDevice(item) {
            this.$emit("scan-device", item)
    }
  }
}

</script>

<style scoped>

</style>
