<template>
  <nav class="fixed top-0 left-0 right-0 bg-white shadow-md z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 sm:space-x-3 z-10">
          <div class="bg-primary-600 p-1.5 sm:p-2 rounded-lg">
            <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="text-lg sm:text-xl font-bold text-gray-900">
            TalentBridge <span class="text-primary-600">AI</span>
          </span>
        </router-link>

        <!-- Desktop Navigation Links -->
        <div class="hidden lg:flex items-center space-x-6 xl:space-x-8">
          <router-link to="/jobs" class="nav-link">
            Browse Jobs
          </router-link>
          <router-link v-if="authStore.isCandidate" to="/saved-jobs" class="nav-link">
            <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
            Saved
          </router-link>
          <router-link v-if="authStore.isRecruiter" to="/post-job" class="nav-link">
            <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Post Job
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="nav-link">
            Dashboard
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/interviews" class="nav-link">
            <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            Interviews
          </router-link>
          <router-link v-if="authStore.isAuthenticated" to="/ai-assistant" class="nav-link-highlight">
            <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            AI Assistant
          </router-link>
        </div>

        <!-- Right Side: Notification + Auth/Profile -->
        <div class="flex items-center space-x-3 sm:space-x-4 z-10">
          <!-- Notification Bell (desktop only, authenticated) -->
          <NotificationBell v-if="authStore.isAuthenticated" class="hidden sm:block" />

          <!-- Auth Buttons (desktop) -->
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="hidden sm:inline-block text-gray-700 hover:text-primary-600 font-medium transition">
              Sign In
            </router-link>
            <router-link to="/register" class="btn-primary btn-sm">
              Get Started
            </router-link>
          </template>

          <!-- Profile Menu (desktop) -->
          <div v-else class="relative hidden lg:block">
            <button @click="showProfileMenu = !showProfileMenu" class="flex items-center space-x-2 hover:opacity-80 transition">
              <div class="w-9 h-9 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center ring-2 ring-primary-100">
                <span class="text-white font-semibold text-sm">
                  {{ authStore.user?.email?.[0].toUpperCase() }}
                </span>
              </div>
              <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </button>

            <!-- Desktop Dropdown Menu -->
            <transition name="dropdown">
              <div v-if="showProfileMenu" class="absolute right-0 mt-3 w-56 bg-white rounded-xl shadow-xl py-2 border border-gray-100">
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-semibold text-gray-900">{{ authStore.user?.email }}</p>
                  <p class="text-xs text-gray-500 capitalize mt-1">{{ authStore.user?.role }}</p>
                </div>
                <router-link to="/profile" class="dropdown-item" @click="showProfileMenu = false">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  Profile
                </router-link>
                <router-link to="/dashboard" class="dropdown-item" @click="showProfileMenu = false">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                  </svg>
                  Dashboard
                </router-link>
                <router-link v-if="authStore.isCandidate" to="/saved-jobs" class="dropdown-item" @click="showProfileMenu = false">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
                  </svg>
                  Saved Jobs
                </router-link>
                <div class="border-t border-gray-100 my-2"></div>
                <button @click="handleLogout" class="dropdown-item text-red-600 hover:bg-red-50 w-full text-left">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                  </svg>
                  Sign Out
                </button>
              </div>
            </transition>
          </div>

          <!-- Mobile Menu Button -->
          <button @click="showMobileMenu = !showMobileMenu" class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition">
            <svg v-if="!showMobileMenu" class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
            <svg v-else class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition name="slide">
      <div v-if="showMobileMenu" class="lg:hidden bg-white border-t border-gray-200 shadow-lg">
        <div class="px-4 py-4 space-y-3 max-h-[calc(100vh-4rem)] overflow-y-auto">
          <!-- User Info (if authenticated) -->
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-3 pb-4 border-b border-gray-200">
            <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
              <span class="text-white font-bold text-lg">
                {{ authStore.user?.email?.[0].toUpperCase() }}
              </span>
            </div>
            <div>
              <p class="font-semibold text-gray-900">{{ authStore.user?.email }}</p>
              <p class="text-sm text-gray-500 capitalize">{{ authStore.user?.role }}</p>
            </div>
          </div>

          <!-- Navigation Links -->
          <router-link to="/jobs" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Browse Jobs
          </router-link>

          <router-link v-if="authStore.isCandidate" to="/saved-jobs" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
            Saved Jobs
          </router-link>

          <router-link v-if="authStore.isRecruiter" to="/post-job" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Post Job
          </router-link>

          <router-link v-if="authStore.isAuthenticated" to="/dashboard" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
            Dashboard
          </router-link>

          <router-link v-if="authStore.isAuthenticated" to="/interviews" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            Interviews
          </router-link>

          <router-link v-if="authStore.isAuthenticated" to="/ai-assistant" class="mobile-nav-item-highlight" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            AI Assistant
            <span class="badge badge-primary ml-auto">AI</span>
          </router-link>

          <router-link v-if="authStore.isAuthenticated" to="/profile" class="mobile-nav-item" @click="showMobileMenu = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            Profile
          </router-link>

          <!-- Auth Buttons (mobile) -->
          <template v-if="!authStore.isAuthenticated">
            <div class="pt-4 border-t border-gray-200 space-y-2">
              <router-link to="/login" class="block w-full btn-secondary text-center" @click="showMobileMenu = false">
                Sign In
              </router-link>
              <router-link to="/register" class="block w-full btn-primary text-center" @click="showMobileMenu = false">
                Get Started
              </router-link>
            </div>
          </template>

          <!-- Logout (mobile) -->
          <button v-else @click="handleLogout" class="mobile-nav-item text-red-600 hover:bg-red-50 w-full">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Sign Out
          </button>
        </div>
      </div>
    </transition>
  </nav>

  <!-- Spacer to prevent content from hiding behind fixed navbar -->
  <div class="h-16"></div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter, useRoute } from 'vue-router'
import NotificationBell from './NotificationBell.vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const showProfileMenu = ref(false)
const showMobileMenu = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => {
  showMobileMenu.value = false
  showProfileMenu.value = false
})

// Close menus when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showProfileMenu.value = false
  }
}

// Add event listener for closing menus
if (typeof window !== 'undefined') {
  window.addEventListener('click', handleClickOutside)
}

const handleLogout = () => {
  authStore.logout()
  showProfileMenu.value = false
  showMobileMenu.value = false
  router.push('/login')
}
</script>

<style scoped>
/* Desktop Nav Links */
.nav-link {
  @apply text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200 text-sm xl:text-base;
}

.nav-link-highlight {
  @apply text-primary-600 hover:text-primary-700 font-semibold transition-colors duration-200 bg-primary-50 px-3 py-1.5 rounded-lg text-sm xl:text-base;
}

/* Dropdown */
.dropdown-item {
  @apply flex items-center space-x-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150;
}

/* Mobile Nav Links */
.mobile-nav-item {
  @apply flex items-center space-x-3 px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-150 font-medium;
}

.mobile-nav-item-highlight {
  @apply flex items-center space-x-3 px-4 py-3 text-primary-700 bg-primary-50 rounded-lg transition-colors duration-150 font-semibold;
}

/* Animations */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style>
