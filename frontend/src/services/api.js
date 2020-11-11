import axios from 'axios'

axios.interceptors.request.use(
    (config) => {
      let token = localStorage.getItem('lds-user-token');
  
      if (token) {
        config.headers['Authorization'] = token;
      }
  
      return config;
    }, 
  
    (error) => {
      return Promise.reject(error);
    }
  );

export default {
    async getDevices() {
        try {
            const response = await axios.get('/api/devices')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getDevice(id) {
        try {
            const response = await axios.get('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getLocations() {
        try {
            const response = await axios.get('/api/locations')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async scanDevice(id){
        try {
            const response = await axios.get('/api/scan/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async scanAll(){
        try {
            const response = await axios.get('/api/scan')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async addDevice(id){
        try {
            const response = await axios.post('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async removeDevice(id){
        try {
            const response = await axios.delete('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getLogs(){
        try {
            const response = await axios.get('/api/history')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async login(username,password){
        let axiosConfig = { 
            headers : {
                'username': username,
                'password': password
            }
        };
        let data = {}
        try {
            const response = await axios.post('/api/login', data, axiosConfig)
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async checkAuth(){
        try {
            const response = await axios.get('/api/login')
            return response
        } catch (error) {
            return error.response
        }
    },
    async getUsers(){
        try {
            const response = await axios.get('/api/users')
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async updateUser(username,password){
        let axiosConfig = { 
            headers : {
                'username': username,
                'password': password
            }
        };
        let data = {}
        try {
            const response = await axios.post('/api/users', data, axiosConfig)
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async removeUser(username){
        let axiosConfig = { 
            headers : {
                'username': username,
            }
        };
        try {
            const response = await axios.delete('/api/users', axiosConfig)
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    }
}
