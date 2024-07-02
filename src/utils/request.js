import axios from "axios";
import {ElMessage} from "element-plus";

const baseURL = '/api'
const instance = axios.create({baseURL})

instance.interceptors.request.use(
    (config) => {
        return config
    },
    (err) => {
        return Promise.reject(err)
        // return false
    }
)
instance.interceptors.response.use(
    result => {
        return result.data;
    },
    err => {
        console.log(err)
        ElMessage.error('serve error')
        return Promise.reject(err)
    }
)


export default instance