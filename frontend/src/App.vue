<template>
  <div id="app">
    <template v-if="loading_devices">
      <div class="d-flex justify-content-center m-5">
        <b-spinner large label="Loading..."></b-spinner>
      </div>
    </template>
    <div v-show="!(loading_devices)" class="main" :key="renderKey">
        <NavBar 
          v-on:scan-all="scanAll" 
          v-on:modify-device="modifyDevice"
        />
        <div v-for="location in locations" :key="location" class="locations">
          <Location 
            :location="location" 
            :devices="devices"
            v-on:scan-device="scanDevice"
          />
        </div>
      </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar';
import Location from './components/Location';
import Api from '@/services/api';

export default {
  name: 'App',
  components: {
    NavBar,
    Location
  },
  methods: {
    toast(message,header){
      this.$bvToast.toast(message, {
          title: header,
          autoHideDelay: 3000})
    },

    async scanDevice(item){
      this.toast(('Scanning ' + item),'Notification');
      await Api.scanDevice(item)
      .then(async (device) => {
        await this.refreshData()
        this.toast(
          (device[0].id + ' is ' + this.convertCode(device[0].ping_code)),
          'Notification')
      })
      .catch(error => {this.toast("Scan Failed, see logs","Notification");console.log(error)})
    },

    convertCode(code){
      if (code == 0){
        return 'Up'
      }
      if (code == 1){
        return 'Not Found'
      }
      if (code == 2){
        return 'Down'
      }
    },

    async scanAll(){
      this.toast("Scanning All","Notification")
      await Api.scanAll()
      .then(async () => {
        await this.refreshData();
        this.toast("Scan Completed","Notification")
      })
      .catch(error => {this.toast("Scan Failed, see logs","Notification");console.log(error)})
    },

    async refreshData(){
      await Api.getDevices()
      .then(
        devices => {
          this.devices = devices
      })
      .catch(error => console.log(error))
      .finally(() => {
        this.renderKey++;
      });
    },
    async modifyDevice(device){
      if (device.modify == "Add"){
        await Api.addDevice(device.id).then(async () => {
          await this.scanDevice(device.id);
        }).catch(error => console.log(error))
      }
      else if (device.modify == "Remove"){
        await Api.removeDevice(device.id).then(async () => {
          await this.refreshData().then(() => {
            this.toast(("Removed " + device.id), "Notification")
          }).catch(error => console.log(error))
        }).catch(error => console.log(error))
      }
    }
  },
  data() {
      return {
          loading_devices: true,
          devices: [],
          loading_locaitons: true,
          locations: [],
          renderKey: 0
      };
  },

  created() {
    Api.getDevices()
      .then(
        devices => {
          this.devices = devices
        })
      .catch(error => console.log(error))
      .finally(() => {
        this.loading_devices = false
      });
    
    Api.getLocations()
      .then(locations => {
        this.locations = locations
      })
      .catch(error => console.log(error))
      .finally(() => {
        this.loading_locations = false
    });
  },

  mounted() {
    this.interval = setInterval(function(){
      this.refreshData()}
    .bind(this),60000);
  },

  beforeDestroy () {
       clearInterval(this.interval)
  },

  computed: {
    show() {
      if (this.loading_devices === true || this.loading_locations === true){
        return false
      }
      else {
        return true
      }
    }
  }
}
</script>

<style>

body {
    background-color: #E5E4E2;
}
a, a:link, a:visited, a:active {
    color: inherit;
    text-decoration: none;
}
a:hover{
    color: inherit;
    text-decoration: underline;
}
.pointer {
    cursor: pointer;
}
.up {
  background-color: rgb(50, 150, 50);
  color: rgb(50, 150, 50);
}
.down {
  background-color: rgb(200, 50, 50);
  color: rgb(200, 50, 50);
}
.dns {
  background-color: rgb(200, 175, 25);
  color: rgb(200, 175, 25);
}
</style>
