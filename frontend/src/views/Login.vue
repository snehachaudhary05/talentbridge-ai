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
          <span class="text-2xl font-bold text-gray-900">TalentBridge<span class="text-primary-600">AI</span></span>
        </router-link>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">Welcome back</h2>
        <p class="mt-2 text-gray-600">Sign in to your account</p>
      </div>

      <div class="bg-white py-8 px-6 shadow-xl rounded-2xl">

        <!-- Login Mode Toggle -->
        <div class="flex rounded-lg border border-gray-200 p-1 mb-6">
          <button
            @click="loginMode = 'password'; resetState()"
            :class="['flex-1 py-2 text-sm font-medium rounded-md transition-all', loginMode === 'password' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:text-gray-900']"
          >Password</button>
          <button
            @click="loginMode = 'otp'; resetState()"
            :class="['flex-1 py-2 text-sm font-medium rounded-md transition-all', loginMode === 'otp' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:text-gray-900']"
          >Login with OTP</button>
        </div>

        <!-- Error / Success -->
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm mb-4">
          {{ error }}
          <div v-if="notVerified" class="mt-2">
            <button @click="handleResendVerification" class="text-primary-600 font-medium underline text-sm">
              Click here to resend verification OTP
            </button>
          </div>
        </div>
        <!-- OTP Verification after resend -->
        <div v-if="showVerifyOTP" class="bg-blue-50 border border-blue-200 px-4 py-4 rounded-lg mb-4 space-y-3">
          <p class="text-sm text-blue-700 font-medium">Enter the verification OTP sent to your email:</p>
          <input
            v-model="verifyOtp"
            type="text"
            maxlength="6"
            class="input-field text-center text-xl tracking-widest font-bold"
            placeholder="------"
            @input="verifyOtp = verifyOtp.replace(/\D/g, '')"
          />
          <button @click="handleVerifyAccount" :disabled="verifyOtp.length !== 6 || loading"
            class="w-full btn-primary text-sm py-2">
            Verify Account
          </button>
        </div>
        <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-lg text-sm mb-4">{{ successMsg }}</div>

        <!-- PASSWORD LOGIN -->
        <form v-if="loginMode === 'password'" @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email address</label>
            <input id="email" v-model="form.email" type="email" required class="input-field" placeholder="you@example.com" />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input id="password" v-model="form.password" type="password" required class="input-field" placeholder="••••••••" />
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input id="remember-me" v-model="form.rememberMe" type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">Remember me</label>
            </div>
          </div>
          <button type="submit" :disabled="loading" class="w-full btn-primary flex items-center justify-center">
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

        <!-- OTP LOGIN -->
        <div v-if="loginMode === 'otp'" class="space-y-4">

          <!-- Step 1: Enter email & request OTP -->
          <div v-if="!otpSent">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email address</label>
              <input v-model="form.email" type="email" required class="input-field" placeholder="you@example.com" />
            </div>
            <button @click="handleRequestOTP" :disabled="loading || !form.email" class="w-full btn-primary flex items-center justify-center mt-4">
              <span v-if="!loading">Send OTP</span>
              <span v-else class="flex items-center">
                <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
              </span>
            </button>
          </div>

          <!-- Step 2: Enter OTP -->
          <div v-else>
            <p class="text-sm text-gray-600 mb-4">OTP sent to <strong>{{ form.email }}</strong></p>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Enter OTP</label>
              <input
                v-model="otp"
                type="text"
                maxlength="6"
                class="input-field text-center text-2xl tracking-widest font-bold"
                placeholder="------"
                @input="otp = otp.replace(/\D/g, '')"
              />
            </div>
            <button @click="handleVerifyLoginOTP" :disabled="loading || otp.length !== 6" class="w-full btn-primary flex items-center justify-center mt-4">
              <span v-if="!loading">Verify & Sign in</span>
              <span v-else class="flex items-center">
                <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Verifying...
              </span>
            </button>
            <div class="text-center text-sm text-gray-500 mt-3">
              Didn't receive it?
              <button @click="handleRequestOTP" class="text-primary-600 hover:text-primary-500 font-medium ml-1">Resend OTP</button>
            </div>
          </div>
        </div>

        <!-- Sign up link -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-gray-300"></div></div>
            <div class="relative flex justify-center text-sm"><span class="px-2 bg-white text-gray-500">New to TalentBridgeAI?</span></div>
          </div>
          <div class="mt-6">
            <router-link to="/register" class="w-full btn-secondary flex items-center justify-center">Create an account</router-link>
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

const loginMode = ref('password') // 'password' or 'otp'
const form = ref({ email: '', password: '', rememberMe: false })
const loading = ref(false)
const error = ref('')
const successMsg = ref('')
const otp = ref('')
const otpSent = ref(false)
const notVerified = ref(false)
const showVerifyOTP = ref(false)
const verifyOtp = ref('')

const resetState = () => {
  error.value = ''
  successMsg.value = ''
  otp.value = ''
  otpSent.value = false
  notVerified.value = false
  showVerifyOTP.value = false
  verifyOtp.value = ''
}

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  notVerified.value = false
  showVerifyOTP.value = false
  try {
    const result = await authStore.login(form.value.email, form.value.password)
    if (result.success) {
      router.push(route.query.redirect || '/dashboard')
    } else {
      const errMsg = result.error?.detail || result.error?.non_field_errors?.[0] || 'Invalid email or password'
      error.value = errMsg
      if (errMsg.toLowerCase().includes('not verified')) {
        notVerified.value = true
      }
    }
  } catch {
    error.value = 'An error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}

const handleResendVerification = async () => {
  successMsg.value = ''
  error.value = ''
  const result = await authStore.resendOTP(form.value.email, 'registration')
  if (result.success) {
    showVerifyOTP.value = true
    notVerified.value = false
    successMsg.value = 'OTP sent! Check your email.'
  } else {
    error.value = 'Failed to send OTP. Try again.'
  }
}

const handleVerifyAccount = async () => {
  loading.value = true
  error.value = ''
  const result = await authStore.verifyOTP(form.value.email, verifyOtp.value)
  if (result.success) {
    showVerifyOTP.value = false
    successMsg.value = 'Email verified! You can now login.'
    verifyOtp.value = ''
  } else {
    error.value = result.error
  }
  loading.value = false
}

const handleRequestOTP = async () => {
  loading.value = true
  error.value = ''
  successMsg.value = ''
  const result = await authStore.requestLoginOTP(form.value.email)
  if (result.success) {
    otpSent.value = true
    successMsg.value = 'OTP sent! Check your email.'
  } else {
    error.value = result.error
  }
  loading.value = false
}

const handleVerifyLoginOTP = async () => {
  loading.value = true
  error.value = ''
  const result = await authStore.verifyLoginOTP(form.value.email, otp.value)
  if (result.success) {
    router.push(route.query.redirect || '/dashboard')
  } else {
    error.value = result.error
  }
  loading.value = false
}
</script>
