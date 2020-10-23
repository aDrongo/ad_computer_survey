<template>
  <div class="Location m-1" :id='location'>
    <div class="row m-2">
      <div class="col-">
      <b-button v-b-toggle="'collapse-' + removeSpace(location)">
        {{location}}
      </b-button>
      </div>
      <div class="col-">
      <DevicesOverview v-bind:devices="devices" v-bind:location="location" v-on:scan-device="emitScanDevice"/>
      </div>
    </div>
    <b-collapse :id="'collapse-' + removeSpace(location)">
      <Devices v-bind:devices="devices" v-bind:location="location" v-on:scan-device="emitScanDevice" />
    </b-collapse>
  </div>
</template>

<script>
import Devices from './Devices';
import DevicesOverview from './DevicesOverview';

export default {
  name: 'Location',
  components: {
    Devices,
    DevicesOverview
  },
  props: ["devices","location"],
  methods: {
    emitScanDevice(item) {
            this.$emit("scan-device", item)
    },
    removeSpace(string) {
      return string.replace(" ","-")
    }
  }
}

</script>

<style scoped>
.collapsed > .when-open,
.not-collapsed > .when-closed {
  display: none;
}
.btn{
  display: inherit;
}

</style>
