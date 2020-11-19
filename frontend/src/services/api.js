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
            const response = await axios.get('/devices')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getDevice(id) {
        try {
            const response = await axios.get('/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getLocations() {
        try {
            const response = await axios.get('/locations')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async scanDevice(id){
        try {
            const response = await axios.get('/scan/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async scanAll(){
        try {
            const response = await axios.get('/scan')
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async addDevice(id){
        try {
            const response = await axios.post('/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async removeDevice(id){
        try {
            const response = await axios.delete('/device/' + id)
            return response.data
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async getLogs(){
        try {
            const response = await axios.get('/history')
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
            const response = await axios.post('/login', data, axiosConfig)
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    },
    async checkAuth(){
        try {
            const response = await axios.get('/login')
            return response
        } catch (error) {
            return error.response
        }
    },
    async getUsers(){
        try {
            const response = await axios.get('/users')
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
            const response = await axios.post('/users', data, axiosConfig)
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
            const response = await axios.delete('/users', axiosConfig)
            return response
        } catch (error) {
            console.log(error.response)
            return error.response
        }
    }
}
