import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import axios from 'axios'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)

// Initialize auth after pinia is set up
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
app.config.globalProperties.$authStore = authStore
authStore.initializeAuth()

// Add axios interceptor to ensure Authorization header is always included
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add axios response interceptor to handle 401 errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be invalid or expired
      console.error('Authentication error - token might be invalid or expired')
      console.error('Error details:', error.response?.data)
    }
    return Promise.reject(error)
  }
)

app.mount('#app')
