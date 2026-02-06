<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <router-link to="/" class="inline-flex items-center space-x-2">
          <div class="bg-primary-600 p-3 rounded-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="text-2xl font-bold text-gray-900">JobPortal<span class="text-primary-600">AI</span></span>
        </router-link>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">Welcome back</h2>
        <p class="mt-2 text-gray-600">Sign in to your account</p>
      </div>

      <!-- Login Form -->
      <div class="bg-white py-8 px-6 shadow-xl rounded-2xl">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email address
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              placeholder="you@example.com"
            />
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field"
              placeholder="••••••••"
            />
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="form.rememberMe"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                Remember me
              </label>
            </div>
            <a href="#" class="text-sm font-medium text-primary-600 hover:text-primary-500">
              Forgot password?
            </a>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary flex items-center justify-center"
          >
            <span v-if="!loading">Sign in</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
          </button>
        </form>

        <!-- Divider -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">New to JobPortalAI?</span>
            </div>
          </div>

          <div class="mt-6">
            <router-link to="/register" class="w-full btn-secondary flex items-center justify-center">
              Create an account
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
  rememberMe: false
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await authStore.login(form.value.email, form.value.password)

    if (result.success) {
      const redirect = route.query.redirect || '/dashboard'
      router.push(redirect)
    } else {
      error.value = result.error?.detail || 'Invalid email or password'
    }
  } catch (err) {
    error.value = 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
