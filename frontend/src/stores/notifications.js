/**
 * Notification Store for managing activities and notifications
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { auditAPI } from '@/services/api'

export const useNotificationStore = defineStore('notifications', () => {
  // State
  const notifications = ref([])
  const recentActivities = ref([])
  const loading = ref(false)
  const error = ref(null)
  const lastFetch = ref(null)
  const refreshTimer = ref(null)

  // Computed
  const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.is_read).length
  })

  const hasHighPriorityNotifications = computed(() => {
    return notifications.value.some(n =>
      !n.is_read && (n.priority === 'high' || n.priority === 'critical')
    )
  })

  const criticalNotifications = computed(() => {
    return notifications.value.filter(n =>
      !n.is_read && n.priority === 'critical'
    )
  })

  // Actions
  const fetchNotifications = async () => {
    if (loading.value) return

    try {
      loading.value = true
      error.value = null

      const response = await auditAPI.getNotifications()

      if (response.data) {
        notifications.value = response.data.notifications || []
        recentActivities.value = response.data.recent_activities || []
        lastFetch.value = new Date()
      }
    } catch (err) {
      console.error('Error fetching notifications:', err)
      error.value = 'دریافت اعلان‌ها در حال حاضر ممکن نیست. بعداً دوباره تلاش کنید.'
      notifications.value = []
      recentActivities.value = []
    } finally {
      loading.value = false
    }
  }

  const markAsRead = async (activityIds = []) => {
    try {
      await auditAPI.markAsRead(activityIds)

      // Update local state
      if (activityIds.length > 0) {
        notifications.value.forEach(notification => {
          if (activityIds.includes(notification.id)) {
            notification.is_read = true
          }
        })
      } else {
        // Mark all as read
        notifications.value.forEach(notification => {
          notification.is_read = true
        })
      }

      return { success: true }
    } catch (err) {
      console.error('Error marking as read:', err)
      return { success: false, error: err.message }
    }
  }

  const getRecentActivities = async (limit = 20) => {
    try {
      const response = await auditAPI.getRecentActivities({ limit })

      recentActivities.value = response.data || []
      return response.data
    } catch (err) {
      console.error('Error fetching recent activities:', err)
      return []
    }
  }

  const getActivitySummary = async (days = 7) => {
    try {
      const response = await auditAPI.getActivitySummary({ days })

      return response.data?.data || {}
    } catch (err) {
      console.error('Error fetching activity summary:', err)
      return {}
    }
  }

  const showWebNotification = (title, options = {}) => {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications')
      return
    }

    if (Notification.permission === 'granted') {
      const notification = new Notification(title, {
        icon: '/favicon.png',
        badge: '/favicon.png',
        dir: 'rtl',
        lang: 'fa',
        ...options
      })

      // Auto close after 5 seconds
      setTimeout(() => {
        notification.close()
      }, 5000)

      return notification
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          showWebNotification(title, options)
        }
      })
    }
  }

  const requestNotificationPermission = async () => {
    if (!('Notification' in window)) {
      return 'not-supported'
    }

    if (Notification.permission === 'default') {
      const permission = await Notification.requestPermission()
      return permission
    }

    return Notification.permission
  }

  const startPeriodicRefresh = (interval = 30000) => {
    // Stop existing timer
    stopPeriodicRefresh()

    // Set up new timer
    refreshTimer.value = setInterval(async () => {
      const oldUnreadCount = unreadCount.value
      await fetchNotifications()

      // Show web notification for new critical notifications
      const newUnreadCount = unreadCount.value
      if (newUnreadCount > oldUnreadCount) {
        const newCritical = criticalNotifications.value.filter(n =>
          !n.notification_sent
        )

        newCritical.forEach(notification => {
          showWebNotification(notification.title, {
            body: `${notification.user_name} • ${notification.formatted_time}`,
            tag: `activity-${notification.id}`,
            requireInteraction: notification.priority === 'critical'
          })
        })
      }
    }, interval)
  }

  const stopPeriodicRefresh = () => {
    if (refreshTimer.value) {
      clearInterval(refreshTimer.value)
      refreshTimer.value = null
    }
  }

  const logActivity = async (activityData) => {
    try {
      // This would be called by other parts of the application
      // to log new activities
      const response = await auditAPI.getActivities() // Note: This should be a POST to create activity
      // TODO: Add createActivity method to auditAPI when backend supports it

      // Refresh notifications after logging new activity
      await fetchNotifications()

      return response.data
    } catch (err) {
      console.error('Error logging activity:', err)
      return null
    }
  }

  const clearAllNotifications = () => {
    notifications.value = []
    recentActivities.value = []
  }

  const updateNotificationPreferences = async (preferences) => {
    try {
      // Update user's notification preferences
      // TODO: Use authAPI.updateProfile when available
      console.log('Updating notification preferences:', preferences)
      // For now, just return success
      return { success: true }
    } catch (err) {
      console.error('Error updating notification preferences:', err)
      return { success: false, error: err.message }
    }
  }

  // Initialize store
  const initialize = async () => {
    await requestNotificationPermission()
    await fetchNotifications()
  }

  return {
    // State
    notifications,
    recentActivities,
    loading,
    error,
    lastFetch,

    // Computed
    unreadCount,
    hasHighPriorityNotifications,
    criticalNotifications,

    // Actions
    fetchNotifications,
    markAsRead,
    getRecentActivities,
    getActivitySummary,
    showWebNotification,
    requestNotificationPermission,
    startPeriodicRefresh,
    stopPeriodicRefresh,
    logActivity,
    clearAllNotifications,
    updateNotificationPreferences,
    initialize
  }
})
