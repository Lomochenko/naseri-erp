<template>
  <div class="relative" ref="dropdownRef">
    <button
      class="relative flex items-center justify-center text-gray-500 transition-colors bg-white border border-gray-200 rounded-full hover:text-dark-900 h-11 w-11 hover:bg-gray-100 hover:text-gray-700 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white"
      @click="toggleDropdown"
    >
      <span
        :class="{ hidden: unreadCount === 0, flex: unreadCount > 0 }"
        class="absolute right-0 top-0.5 z-1 h-2 w-2 rounded-full bg-orange-400"
      >
        <span
          class="absolute inline-flex w-full h-full bg-orange-400 rounded-full opacity-75 -z-1 animate-ping"
        ></span>
      </span>

      <!-- Notification count badge -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center min-w-5"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>

      <svg
        class="fill-current"
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M10.75 2.29248C10.75 1.87827 10.4143 1.54248 10 1.54248C9.58583 1.54248 9.25004 1.87827 9.25004 2.29248V2.83613C6.08266 3.20733 3.62504 5.9004 3.62504 9.16748V14.4591H3.33337C2.91916 14.4591 2.58337 14.7949 2.58337 15.2091C2.58337 15.6234 2.91916 15.9591 3.33337 15.9591H4.37504H15.625H16.6667C17.0809 15.9591 17.4167 15.6234 17.4167 15.2091C17.4167 14.7949 17.0809 14.4591 16.6667 14.4591H16.375V9.16748C16.375 5.9004 13.9174 3.20733 10.75 2.83613V2.29248ZM14.875 14.4591V9.16748C14.875 6.47509 12.6924 4.29248 10 4.29248C7.30765 4.29248 5.12504 6.47509 5.12504 9.16748V14.4591H14.875ZM8.00004 17.7085C8.00004 18.1228 8.33583 18.4585 8.75004 18.4585H11.25C11.6643 18.4585 12 18.1228 12 17.7085C12 17.2943 11.6643 16.9585 11.25 16.9585H8.75004C8.33583 16.9585 8.00004 17.2943 8.00004 17.7085Z"
          fill=""
        />
      </svg>
    </button>

    <!-- Dropdown Start -->
    <div
      v-if="dropdownOpen"
      class="absolute -right-[240px] mt-[17px] flex h-[500px] w-[380px] flex-col rounded-2xl border border-gray-200 bg-white p-3 shadow-theme-lg dark:border-gray-800 dark:bg-gray-dark sm:w-[400px] lg:right-0"
    >
      <!-- Header -->
      <div
        class="flex items-center justify-between pb-3 mb-3 border-b border-gray-100 dark:border-gray-800"
      >
        <h5 class="text-lg font-semibold text-gray-800 dark:text-white/90">
          اعلانات و فعالیت‌ها
        </h5>

        <div class="flex items-center gap-2">
          <!-- Mark all as read button -->
          <button
            v-if="unreadCount > 0"
            @click="markAllAsRead"
            :disabled="markingAsRead"
            class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 disabled:opacity-50"
          >
            همه را خوانده علامت‌گذاری کن
          </button>

          <!-- Close button -->
          <button @click="closeDropdown" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
            <svg
              class="fill-current"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M6.21967 7.28131C5.92678 6.98841 5.92678 6.51354 6.21967 6.22065C6.51256 5.92775 6.98744 5.92775 7.28033 6.22065L11.999 10.9393L16.7176 6.22078C17.0105 5.92789 17.4854 5.92788 17.7782 6.22078C18.0711 6.51367 18.0711 6.98855 17.7782 7.28144L13.0597 12L17.7782 16.7186C18.0711 17.0115 18.0711 17.4863 17.7782 17.7792C17.4854 18.0721 17.0105 18.0721 16.7176 17.7792L11.999 13.0607L7.28033 17.7794C6.98744 18.0722 6.51256 18.0722 6.21967 17.7794C5.92678 17.4865 5.92678 17.0116 6.21967 16.7187L10.9384 12L6.21967 7.28131Z"
                fill=""
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex mb-3 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
        <button
          @click="activeTab = 'notifications'"
          :class="[
            'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
            activeTab === 'notifications'
              ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          اعلانات ({{ unreadCount }})
        </button>
        <button
          @click="activeTab = 'activities'"
          :class="[
            'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
            activeTab === 'activities'
              ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          آخرین فعالیت‌ها
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <div class="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full"></div>
        <span class="mr-3 text-gray-600 dark:text-gray-400">در حال بارگذاری...</span>
      </div>

      <!-- Content -->
      <div v-else class="flex-1 overflow-hidden">
        <!-- Notifications Tab -->
        <div v-if="activeTab === 'notifications'" class="h-full overflow-y-auto custom-scrollbar">
          <div v-if="notifications.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
            <svg class="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4 4h9l7 7v3"></path>
            </svg>
            اعلان جدیدی وجود ندارد
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="notification in notifications"
              :key="notification.id"
              @click="handleNotificationClick(notification)"
              class="flex gap-3 p-3 rounded-lg cursor-pointer transition-colors border border-transparent hover:bg-gray-50 dark:hover:bg-gray-800 hover:border-gray-200 dark:hover:border-gray-700"
              :class="{
                'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800': !notification.is_read,
                'opacity-75': notification.is_read
              }"
            >
              <!-- Activity Icon -->
              <div class="flex-shrink-0">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center"
                  :class="getActivityIconClass(notification.activity_type)"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path :d="getActivityIconPath(notification.activity_type)" />
                  </svg>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {{ notification.title }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {{ notification.user_name }} • {{ notification.formatted_time }}
                </p>

                <!-- Priority Badge -->
                <span
                  v-if="notification.priority === 'high' || notification.priority === 'critical'"
                  :class="[
                    'inline-block px-2 py-1 text-xs rounded-full mt-2',
                    notification.priority === 'critical'
                      ? 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
                      : 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400'
                  ]"
                >
                  {{ notification.priority === 'critical' ? 'بحرانی' : 'مهم' }}
                </span>
              </div>

              <!-- Unread indicator -->
              <div v-if="!notification.is_read" class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
            </div>
          </div>
        </div>

        <!-- Activities Tab -->
        <div v-if="activeTab === 'activities'" class="h-full overflow-y-auto custom-scrollbar">
          <div v-if="recentActivities.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
            <svg class="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            فعالیتی ثبت نشده است
          </div>

          <div v-else class="space-y-2">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="flex gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <!-- Activity Icon -->
              <div class="flex-shrink-0">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center"
                  :class="getActivityIconClass(activity.activity_type)"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path :d="getActivityIconPath(activity.activity_type)" />
                  </svg>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ activity.title }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {{ activity.user_name }} • {{ activity.formatted_time }}
                </p>

                <!-- Activity Type Badge -->
                <span class="inline-block px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full mt-2">
                  {{ activity.activity_type_display }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="border-t border-gray-200 dark:border-gray-700 pt-3 mt-3">
        <router-link
          to="/reports"
          class="w-full flex justify-center rounded-lg border border-gray-300 bg-white p-3 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-200"
          @click="closeDropdown"
        >
          مشاهده همه فعالیت‌ها
        </router-link>
      </div>
    </div>
    <!-- Dropdown End -->
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notifications'

const router = useRouter()
const notificationStore = useNotificationStore()

// Component state
const dropdownOpen = ref(false)
const dropdownRef = ref(null)
const activeTab = ref('notifications')
const loading = ref(false)
const markingAsRead = ref(false)

// Computed properties
const notifications = computed(() => notificationStore.notifications)
const recentActivities = computed(() => notificationStore.recentActivities)
const unreadCount = computed(() => notificationStore.unreadCount)

// Methods
const toggleDropdown = async () => {
  dropdownOpen.value = !dropdownOpen.value

  if (dropdownOpen.value) {
    loading.value = true
    await notificationStore.fetchNotifications()
    loading.value = false
  }
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleNotificationClick = async (notification) => {
  // Mark as read
  await notificationStore.markAsRead([notification.id])

  // Handle navigation based on activity type
  handleActivityNavigation(notification)

  closeDropdown()
}

const handleActivityNavigation = (activity) => {
  const navigationMap = {
    'sale_created': () => router.push({ path: '/sales', query: { highlight: activity.object_id } }),
    'sale_confirmed': () => router.push({ path: '/sales', query: { highlight: activity.object_id } }),
    'product_created': () => router.push({ path: '/products', query: { highlight: activity.object_id } }),
    'customer_created': () => router.push({ path: '/sales', query: { customer: activity.object_id } }),
    'stock_low_warning': () => router.push({ path: '/inventory', query: { filter: 'low_stock' } }),
    'payment_received': () => router.push({ path: '/sales', query: { filter: 'payments' } })
  }

  const navigationAction = navigationMap[activity.activity_type]
  if (navigationAction) {
    navigationAction()
  } else {
    // Default navigation to activities page
    router.push('/activities')
  }
}

const markAllAsRead = async () => {
  if (notifications.value.length === 0 || markingAsRead.value) return

  markingAsRead.value = true
  try {
    const unreadIds = notifications.value.filter(n => !n.is_read).map(n => n.id)
    await notificationStore.markAsRead(unreadIds)
  } catch (error) {
    console.error('Error marking all as read:', error)
  } finally {
    markingAsRead.value = false
  }
}

const getActivityIconClass = (activityType) => {
  const iconClasses = {
    'user_login': 'bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400',
    'user_logout': 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    'product_created': 'bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400',
    'product_updated': 'bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400',
    'customer_created': 'bg-purple-100 text-purple-600 dark:bg-purple-900/20 dark:text-purple-400',
    'sale_created': 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400',
    'sale_confirmed': 'bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400',
    'payment_received': 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-400',
    'stock_low_warning': 'bg-red-100 text-red-600 dark:bg-red-900/20 dark:text-red-400',
    'inventory_transaction': 'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/20 dark:text-indigo-400'
  }
  return iconClasses[activityType] || 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
}

const getActivityIconPath = (activityType) => {
  const iconPaths = {
    'user_login': 'M10 2L3 9l7-7 7 7-7-7z',
    'user_logout': 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
    'product_created': 'M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z',
    'customer_created': 'M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z',
    'sale_created': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    'sale_confirmed': 'M5 13l4 4L19 7',
    'payment_received': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'stock_low_warning': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    'inventory_transaction': 'M7 4V2a1 1 0 011-1h4a1 1 0 011 1v2h4a1 1 0 110 2h-1v10a2 2 0 01-2 2H6a2 2 0 01-2-2V6H3a1 1 0 010-2h4zM9 3v1h2V3H9zm2 3H9v8h2V6z'
  }
  return iconPaths[activityType] || 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

// Click outside to close
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)

  // Initial load
  notificationStore.fetchNotifications()

  // Set up periodic refresh
  notificationStore.startPeriodicRefresh()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  notificationStore.stopPeriodicRefresh()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}
</style>
