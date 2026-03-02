import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'
import axios from 'axios'

// Configure axios base URL
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)

// Initialize auth after pinia is set up
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
app.config.globalProperties.$authStore = authStore
authStore.initializeAuth()

// ── Request interceptor: attach Authorization header ──────────────────────────
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ── Response interceptor: auto-refresh on 401 ─────────────────────────────────
let isRefreshing = false
let failedQueue = []   // requests waiting while token is being refreshed

const processQueue = (error, token = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error)
    else resolve(token)
  })
  failedQueue = []
}

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Only handle 401 that hasn't already been retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = localStorage.getItem('refreshToken')

      // No refresh token → log out immediately
      if (!refreshToken) {
        authStore.logout()
        router.push('/login')
        return Promise.reject(error)
      }

      // If a refresh is already in progress, queue this request
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return axios(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      // Start refreshing
      originalRequest._retry = true
      isRefreshing = true

      try {
        const res = await axios.post('/token/refresh/', { refresh: refreshToken })
        const newToken = res.data.access

        // Update stored token
        localStorage.setItem('token', newToken)
        authStore.token = newToken
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`

        processQueue(null, newToken)

        // Retry the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return axios(originalRequest)
      } catch (refreshError) {
        // Refresh failed → session is completely expired
        processQueue(refreshError, null)
        authStore.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

app.mount('#app')
