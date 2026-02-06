<template>
  <div class="relative">
    <!-- Notification Bell Button -->
    <button
      @click="toggleDropdown"
      class="relative p-2 text-gray-700 hover:text-primary-600 transition rounded-full hover:bg-gray-100"
      :class="{ 'animate-pulse': hasUnread }"
    >
      <!-- Bell Icon -->
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>

      <!-- Unread Badge -->
      <span
        v-if="unreadCount > 0"
        class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- Notifications Dropdown -->
    <div
      v-if="showDropdown"
      class="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-xl border border-gray-200 z-50"
      @click.stop
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Notifications</h3>
        <button
          v-if="unreadCount > 0"
          @click="handleMarkAllAsRead"
          class="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Mark all read
        </button>
      </div>

      <!-- Notifications List -->
      <div class="max-h-96 overflow-y-auto">
        <!-- Loading State -->
        <div v-if="loading" class="p-8 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p class="text-gray-500 mt-2">Loading notifications...</p>
        </div>

        <!-- No Notifications -->
        <div v-else-if="notifications.length === 0" class="p-8 text-center">
          <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <p class="text-gray-500 mt-4">No notifications yet</p>
          <p class="text-gray-400 text-sm mt-1">We'll notify you when something arrives</p>
        </div>

        <!-- Notification Items -->
        <div v-else>
          <div
            v-for="notification in notifications"
            :key="notification.id"
            @click="handleNotificationClick(notification)"
            class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition"
            :class="{ 'bg-blue-50': !notification.is_read }"
          >
            <div class="flex items-start">
              <!-- Notification Icon -->
              <div class="flex-shrink-0 mt-1">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center"
                  :class="getNotificationIconClass(notification.notification_type)"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      :d="getNotificationIconPath(notification.notification_type)"
                    />
                  </svg>
                </div>
              </div>

              <!-- Notification Content -->
              <div class="ml-3 flex-1">
                <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                <p class="text-sm text-gray-600 mt-1">{{ notification.message }}</p>
                <p class="text-xs text-gray-400 mt-2">{{ formatTime(notification.created_at) }}</p>
              </div>

              <!-- Unread Indicator -->
              <div v-if="!notification.is_read" class="flex-shrink-0 ml-2">
                <div class="w-2 h-2 bg-blue-600 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="p-3 border-t border-gray-200 text-center">
        <router-link
          to="/notifications"
          @click="showDropdown = false"
          class="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          View all notifications
        </router-link>
      </div>
    </div>

    <!-- Click Outside Handler -->
    <div v-if="showDropdown" @click="showDropdown = false" class="fixed inset-0 z-40"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useNotificationStore } from '../stores/notifications'
import { useRouter } from 'vue-router'

const notificationStore = useNotificationStore()
const router = useRouter()

const showDropdown = ref(false)

// Computed properties
const notifications = computed(() => notificationStore.notifications)
const unreadCount = computed(() => notificationStore.unreadCount)
const hasUnread = computed(() => notificationStore.hasUnread)
const loading = computed(() => notificationStore.loading)

// Toggle dropdown
const toggleDropdown = async () => {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value) {
    await notificationStore.fetchRecentNotifications()
  }
}

// Mark all as read
const handleMarkAllAsRead = async () => {
  await notificationStore.markAllAsRead()
}

// Handle notification click
const handleNotificationClick = async (notification) => {
  // Mark as read
  if (!notification.is_read) {
    await notificationStore.markAsRead(notification.id)
  }

  // Navigate to link if exists
  if (notification.link) {
    showDropdown.value = false
    router.push(notification.link)
  }
}

// Get notification icon class based on type
const getNotificationIconClass = (type) => {
  const iconClasses = {
    'application_submitted': 'bg-green-100 text-green-600',
    'application_status_changed': 'bg-blue-100 text-blue-600',
    'new_application': 'bg-purple-100 text-purple-600',
    'job_match': 'bg-yellow-100 text-yellow-600',
    'resume_viewed': 'bg-pink-100 text-pink-600',
    'interview_scheduled': 'bg-orange-100 text-orange-600',
    'system': 'bg-gray-100 text-gray-600',
  }
  return iconClasses[type] || 'bg-gray-100 text-gray-600'
}

// Get notification icon path based on type
const getNotificationIconPath = (type) => {
  const iconPaths = {
    'application_submitted': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    'application_status_changed': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
    'new_application': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'job_match': 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z',
    'resume_viewed': 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
    'interview_scheduled': 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
  }
  return iconPaths[type] || 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

// Format time
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} min ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`

  return date.toLocaleDateString()
}

// Lifecycle hooks
onMounted(() => {
  notificationStore.startPolling()
})

onUnmounted(() => {
  notificationStore.stopPolling()
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
