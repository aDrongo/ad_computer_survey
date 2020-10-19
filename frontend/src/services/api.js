import axios from 'axios'

export default {
    async getDevices() {
        try {
            const response = await axios.get('/api/devices')
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async getDevice(id) {
        try {
            const response = await axios.get('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async getLocations() {
        try {
            const response = await axios.get('/api/locations')
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async scanDevice(id){
        try {
            const response = await axios.get('/api/scan/' + id)
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async scanAll(){
        try {
            const response = await axios.get('/api/scan')
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async addDevice(id){
        try {
            const response = await axios.post('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async removeDevice(id){
        try {
            const response = await axios.delete('/api/device/' + id)
            return response.data
        } catch (error) {
            console.log(error)
        }
    },
    async getLogs(){
        try {
            const response = await axios.get('/api/logs/json')
            return response.data
        } catch (error) {
            console.log(error)
        }
    }

}