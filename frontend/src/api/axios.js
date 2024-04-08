import axios from "axios";
const backendURL = import.meta.env.VITE_BACKEND_URL;



export default axios.create({
    baseURL: String(backendURL),
    withCredentials: true
})

export const axiosLoginForm = axios.create({
    baseURL: String(backendURL+"/auth/token"),
    headers:{
        'Content-Type': 'multipart/form-data'
    },
    withCredentials: true 
})

export const axiosRegister = axios.create({
    baseURL: String(backendURL+"/auth/register"),
    withCredentials: true
})

export const axiosStartScan = axios.create({
    baseURL: String(backendURL+"/api/start-scan"),
    withCredentials: true
})