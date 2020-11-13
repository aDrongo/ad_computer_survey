<template>
 <div>
   <template v-if="locationDevices.length > 0">
    <div class="Location m-1" :id='location'>
      <div class="d-inline-flex m-1">
        <div>
        <b-button class="text-nowrap" @click="$emit('opened-location', location)">
          {{location}}
        </b-button>
        </div>
        <div>
        <DevicesOverview v-bind:locationDevices="locationDevices" v-bind:location="location" v-on:scan-device="emitScanDevice"/>
        </div>
      </div>
      <b-collapse :id="'collapse-' + removeSpace(location)" :visible="location === opened">
        <Devices v-bind:locationDevices="locationDevices" v-bind:location="location" v-on:scan-device="emitScanDevice" />
      </b-collapse>
    </div>
   </template>
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
  props: ["locationDevices","location","opened"],
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
