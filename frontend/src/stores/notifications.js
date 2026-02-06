import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'  // Backend API URL

export const useNotificationStore = defineStore('notifications', () => {
  const notifications = ref([])
  const unreadCount = ref(0)
  const loading = ref(false)

  // Computed
  const hasUnread = computed(() => unreadCount.value > 0)

  // Get auth token from localStorage
  const getAuthToken = () => {
    const token = localStorage.getItem('access_token')
    return token ? `Bearer ${token}` : null
  }

  // Fetch unread count
  const fetchUnreadCount = async () => {
    try {
      const token = getAuthToken()
      if (!token) return

      const response = await axios.get(`${API_URL}/notifications/unread_count/`, {
        headers: { Authorization: token }
      })
      unreadCount.value = response.data.count
    } catch (error) {
      console.error('Error fetching unread count:', error)
    }
  }

  // Fetch recent notifications
  const fetchRecentNotifications = async () => {
    loading.value = true
    try {
      const token = getAuthToken()
      if (!token) return

      const response = await axios.get(`${API_URL}/notifications/recent/`, {
        headers: { Authorization: token }
      })
      notifications.value = response.data
    } catch (error) {
      console.error('Error fetching notifications:', error)
    } finally {
      loading.value = false
    }
  }

  // Fetch all notifications
  const fetchAllNotifications = async () => {
    loading.value = true
    try {
      const token = getAuthToken()
      if (!token) return

      const response = await axios.get(`${API_URL}/notifications/`, {
        headers: { Authorization: token }
      })
      notifications.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching all notifications:', error)
      return []
    } finally {
      loading.value = false
    }
  }

  // Mark notification as read
  const markAsRead = async (notificationId) => {
    try {
      const token = getAuthToken()
      if (!token) return

      await axios.post(`${API_URL}/notifications/${notificationId}/mark_as_read/`, {}, {
        headers: { Authorization: token }
      })

      // Update local state
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification && !notification.is_read) {
        notification.is_read = true
        unreadCount.value = Math.max(0, unreadCount.value - 1)
      }
    } catch (error) {
      console.error('Error marking notification as read:', error)
    }
  }

  // Mark all as read
  const markAllAsRead = async () => {
    try {
      const token = getAuthToken()
      if (!token) return

      await axios.post(`${API_URL}/notifications/mark_all_as_read/`, {}, {
        headers: { Authorization: token }
      })

      // Update local state
      notifications.value.forEach(n => n.is_read = true)
      unreadCount.value = 0
    } catch (error) {
      console.error('Error marking all as read:', error)
    }
  }

  // Start polling for new notifications (every 30 seconds)
  let pollInterval = null

  const startPolling = () => {
    stopPolling() // Clear any existing interval
    fetchUnreadCount() // Initial fetch
    pollInterval = setInterval(() => {
      fetchUnreadCount()
    }, 30000) // 30 seconds
  }

  const stopPolling = () => {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
  }

  return {
    notifications,
    unreadCount,
    loading,
    hasUnread,
    fetchUnreadCount,
    fetchRecentNotifications,
    fetchAllNotifications,
    markAsRead,
    markAllAsRead,
    startPolling,
    stopPolling
  }
})
