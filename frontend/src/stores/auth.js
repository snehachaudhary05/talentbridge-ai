import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    isCandidate: (state) => state.user?.role === 'candidate',
    isRecruiter: (state) => state.user?.role === 'recruiter',
    isAdmin: (state) => state.user?.role === 'admin',
  },

  actions: {
    async register(email, password, role) {
      try {
        const response = await axios.post(`${API_URL}/accounts/register/`, {
          email,
          password,
          role
        })
        return { success: true, data: response.data }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || 'Registration failed'
        }
      }
    },

    async login(email, password) {
      try {
        const response = await axios.post(`${API_URL}/token/`, {
          email,  // Use 'email' since USERNAME_FIELD = 'email'
          password
        })

        this.token = response.data.access
        this.refreshToken = response.data.refresh

        localStorage.setItem('token', this.token)
        localStorage.setItem('refreshToken', this.refreshToken)

        // Set default auth header
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        // Fetch user profile to get actual role from backend
        try {
          const userResponse = await axios.get(`${API_URL}/accounts/me/`)
          this.user = {
            id: userResponse.data.id,
            email: userResponse.data.email,
            role: userResponse.data.role
          }
          // Store user info in localStorage for persistence
          localStorage.setItem('user', JSON.stringify(this.user))
        } catch (profileError) {
          // Fallback to token-based role if profile fetch fails
          this.user = { email, role: this.getRoleFromToken(this.token) }
        }

        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || 'Login failed'
        }
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },

    getRoleFromToken(token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return payload.role || 'candidate'
      } catch {
        return 'candidate'
      }
    },

    initializeAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        // Try to restore user from localStorage first
        const storedUser = localStorage.getItem('user')
        if (storedUser) {
          try {
            this.user = JSON.parse(storedUser)
          } catch {
            this.user = { role: this.getRoleFromToken(this.token) }
          }
        } else {
          this.user = { role: this.getRoleFromToken(this.token) }
        }
      }
    }
  }
})
