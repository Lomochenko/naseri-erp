<template>
  <AdminLayout>
    <div>
      <!-- Breadcrumb -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 class="text-title-md2 font-bold text-black dark:text-white">
          صفحه تست سیستم
        </h2>
        <nav>
          <ol class="flex items-center gap-2">
            <li>
              <router-link class="font-medium" to="/">داشبورد /</router-link>
            </li>
            <li class="font-medium text-primary">تست سیستم</li>
          </ol>
        </nav>
      </div>

      <!-- System Status -->
      <div class="mb-6 rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <h3 class="text-xl font-semibold text-black dark:text-white mb-4">
          وضعیت سیستم
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
            <div class="flex items-center">
              <svg class="h-6 w-6 text-green-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="text-sm font-medium text-green-800 dark:text-green-200">فرانت‌اند</p>
                <p class="text-xs text-green-600 dark:text-green-400">آماده</p>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-lg" :class="backendStatus.connected ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'">
            <div class="flex items-center">
              <svg v-if="backendStatus.connected" class="h-6 w-6 text-green-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="h-6 w-6 text-red-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <div>
                <p class="text-sm font-medium" :class="backendStatus.connected ? 'text-green-800 dark:text-green-200' : 'text-red-800 dark:text-red-200'">
                  بک‌اند Django
                </p>
                <p class="text-xs" :class="backendStatus.connected ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                  {{ backendStatus.connected ? 'متصل' : 'قطع' }}
                </p>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
            <div class="flex items-center">
              <svg class="h-6 w-6 text-blue-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <div>
                <p class="text-sm font-medium text-blue-800 dark:text-blue-200">احراز هویت</p>
                <p class="text-xs text-blue-600 dark:text-blue-400">
                  {{ authStore.isAuthenticated ? 'وارد شده' : 'خارج' }}
                </p>
              </div>
            </div>
          </div>

          <div class="p-4 rounded-lg bg-purple-50 dark:bg-purple-900/20">
            <div class="flex items-center">
              <svg class="h-6 w-6 text-purple-500 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <div>
                <p class="text-sm font-medium text-purple-800 dark:text-purple-200">RTL</p>
                <p class="text-xs text-purple-600 dark:text-purple-400">فعال</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Test Actions -->
      <div class="mb-6 rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <h3 class="text-xl font-semibold text-black dark:text-white mb-4">
          تست عملکردها
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <button
            @click="testBackendConnection"
            :disabled="isTestingBackend"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            <div class="text-center">
              <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
              </svg>
              <p class="font-medium">تست اتصال بک‌اند</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ isTestingBackend ? 'در حال تست...' : 'کلیک کنید' }}
              </p>
            </div>
          </button>

          <button
            @click="testStores"
            :disabled="isTestingStores"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            <div class="text-center">
              <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
              <p class="font-medium">تست Stores</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ isTestingStores ? 'در حال تست...' : 'کلیک کنید' }}
              </p>
            </div>
          </button>

          <button
            @click="testRouting"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors"
          >
            <div class="text-center">
              <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <p class="font-medium">تست مسیریابی</p>
              <p class="text-sm text-gray-600 dark:text-gray-400">کلیک کنید</p>
            </div>
          </button>
        </div>
      </div>

      <!-- Test Results -->
      <div v-if="testResults.length > 0" class="mb-6 rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <h3 class="text-xl font-semibold text-black dark:text-white mb-4">
          نتایج تست
        </h3>
        
        <div class="space-y-3">
          <div
            v-for="result in testResults"
            :key="result.id"
            class="p-3 rounded-lg"
            :class="result.success ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'"
          >
            <div class="flex items-center">
              <svg
                v-if="result.success"
                class="h-5 w-5 text-green-500 ml-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg
                v-else
                class="h-5 w-5 text-red-500 ml-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <div>
                <p class="font-medium" :class="result.success ? 'text-green-800 dark:text-green-200' : 'text-red-800 dark:text-red-200'">
                  {{ result.name }}
                </p>
                <p class="text-sm" :class="result.success ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                  {{ result.message }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ result.timestamp }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Navigation -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <h3 class="text-xl font-semibold text-black dark:text-white mb-4">
          دسترسی سریع
        </h3>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <router-link
            to="/products"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors text-center"
          >
            <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <p class="font-medium">محصولات</p>
          </router-link>

          <router-link
            to="/sales"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors text-center"
          >
            <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p class="font-medium">فروش</p>
          </router-link>

          <router-link
            to="/customers"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors text-center"
          >
            <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <p class="font-medium">مشتریان</p>
          </router-link>

          <router-link
            to="/inventory"
            class="p-4 rounded-lg border border-stroke hover:bg-gray-50 dark:border-strokedark dark:hover:bg-gray-800 transition-colors text-center"
          >
            <svg class="h-8 w-8 mx-auto mb-2 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
            </svg>
            <p class="font-medium">موجودی</p>
          </router-link>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProductsStore } from '@/stores/products'
import { useSalesStore } from '@/stores/sales'
import { useInventoryStore } from '@/stores/inventory'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()
const productsStore = useProductsStore()
const salesStore = useSalesStore()
const inventoryStore = useInventoryStore()

// State
const backendStatus = ref({
  connected: false,
  lastChecked: null
})

const isTestingBackend = ref(false)
const isTestingStores = ref(false)
const testResults = ref([])

// Methods
const addTestResult = (name, success, message) => {
  testResults.value.unshift({
    id: Date.now(),
    name,
    success,
    message,
    timestamp: new Date().toLocaleTimeString('fa-IR')
  })
}

const testBackendConnection = async () => {
  isTestingBackend.value = true
  
  try {
    // Test basic API connection
    const response = await fetch('http://127.0.0.1:8000/api/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (response.ok) {
      backendStatus.value.connected = true
      backendStatus.value.lastChecked = new Date()
      addTestResult('اتصال بک‌اند', true, 'اتصال با موفقیت برقرار شد')
    } else {
      throw new Error(`HTTP ${response.status}`)
    }
  } catch (error) {
    backendStatus.value.connected = false
    addTestResult('اتصال بک‌اند', false, `خطا: ${error.message}`)
  } finally {
    isTestingBackend.value = false
  }
}

const testStores = async () => {
  isTestingStores.value = true
  
  try {
    // Test auth store
    if (authStore.isAuthenticated) {
      addTestResult('Auth Store', true, 'کاربر وارد شده است')
    } else {
      addTestResult('Auth Store', false, 'کاربر وارد نشده است')
    }
    
    // Test products store
    addTestResult('Products Store', true, `${productsStore.products.length} محصول در store`)
    
    // Test sales store
    addTestResult('Sales Store', true, `${salesStore.customers.length} مشتری در store`)
    
    // Test inventory store
    addTestResult('Inventory Store', true, `${inventoryStore.stockLevels.length} آیتم موجودی در store`)
    
  } catch (error) {
    addTestResult('Stores Test', false, `خطا: ${error.message}`)
  } finally {
    isTestingStores.value = false
  }
}

const testRouting = () => {
  const routes = ['/products', '/sales', '/customers', '/inventory', '/reports']
  
  routes.forEach(route => {
    try {
      router.resolve(route)
      addTestResult(`Route ${route}`, true, 'مسیر معتبر است')
    } catch (error) {
      addTestResult(`Route ${route}`, false, `خطا: ${error.message}`)
    }
  })
}

// Lifecycle
onMounted(() => {
  testBackendConnection()
})
</script>
