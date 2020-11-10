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
          v-on:do-login="login"
          v-on:do-logout="logout"
          v-on:modify-user="modifyUser"
          v-on:pause-timer="pauseTimer"
          :user="user"
        />
        <div v-for="location in locations" :key="location" class="locations">
          <Location 
            :location="location" 
            :locationDevices="getLocationDevices(devices,location)"
            :opened="opened"
            v-on:scan-device="scanDevice"
            v-on:opened-location="openedLocation"
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
  data() {
      return {
          loading_devices: true,
          devices: [],
          loading_locaitons: true,
          locations: [],
          renderKey: 0,
          opened: null,
          user: null
      };
  },
  methods: {
    pauseTimer(pause){
      if (pause){
        console.log('pause')
        clearInterval(this.interval)
      }
      else if (!pause) {
        console.log('unpause')
        this.interval = setInterval(this.intervalFunc(),60000);
      }
    },
    toast(message,header=null){
      if (!header) header = "Notification";
      this.$bvToast.toast(message, {
          title: header,
          autoHideDelay: 3000})
    },

    openedLocation(location){
      if (this.opened === location){
        this.opened = null;
      }
      else {
        this.opened = location;
      }
    },

    getLocationDevices(devices,location){
        var results = []
        for (var i=0; i<devices.length; i++){
            if (devices[i].location == location){
                results.push(devices[i])
            }
        }
        results.sort((a,b) => (a.ping_code < b.ping_code) ? 1 : -1)
        return results
    },

    logout(){
      this.toast(('Logging out ' + this.user),'Notification');
      this.user = null;
      localStorage.setItem('lds-user', null);
      localStorage.setItem('lds-user-token', null)
    },

    async login(form){
      await Api.login(form.username, form.password).then(
        async (response) => {
          if (response.status == 200){
            this.toast(('Welcome ' + form.username),'Notification');
            this.user = form.username;
            localStorage.setItem('lds-user', form.username);
            localStorage.setItem('lds-user-token', response.data.token)
          }
          else if (response.status == 401){
            alert("Incorrect Login")
          }
        }
      )
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
    },

    async refreshData(){
      await Api.getDevices() 
      .then(
        devices => {
          this.devices = devices
      })
      .finally(() => {
        this.renderKey++;
      });
    },

    async modifyDevice(device){
      if (device.modify == "Add"){
        await Api.addDevice(device.id).then(async () => {
          await this.scanDevice(device.id);
        })
      }
      else if (device.modify == "Remove"){
        await Api.removeDevice(device.id).then(async () => {
          await this.refreshData().then(() => {
            this.toast(("Removed " + device.id), "Notification")
          })
        })
      }
    },

    async modifyUser(form){
      if (form.modify == "Add User" || form.modify == "Reset Password"){
        await Api.updateUser(form.username,form.password).then((response) => {
          if (response.status == 200) this.toast("Completed: " + form.modify + " for " + form.username)
        })
      }
      else if (form.modify == "Remove User"){
        await Api.removeUser(form.username).then((response) => {
          if (response.status == 200) this.toast("Completed: " + form.modify + " for " + form.username)
        })
      }
    },
    async intervalFunc(){
      await Api.checkAuth().then((response) => {
        if (response.status == 210){
          if (this.user && this.user != "null"){
            this.logout()
          }
        }
      })
      await this.refreshData()
      }
  },
  created() {
    this.user = localStorage.getItem('lds-user')
    Api.getDevices()
      .then(
        devices => {
          this.devices = devices
        })
      .finally(() => {
        this.loading_devices = false
      });
    
    Api.getLocations()
      .then(locations => {
        this.locations = locations
      })
      .finally(() => {
        this.loading_locations = false
    });
  },

  mounted() {
    this.interval = setInterval(async function() {
      await Api.checkAuth().then((response) => {
        if (response.status == 210){
          if (this.user && this.user != "null"){
            this.logout()
          }
        }
      })
      await this.refreshData()
    }.bind(this),60000);
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
    text-decoration: inherit;
    color: inherit;
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
