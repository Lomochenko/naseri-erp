<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        داشبورد یراقالات ناصری
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li class="font-medium text-primary">داشبورد اصلی</li>
        </ol>
      </nav>
    </div>

    <!-- Welcome Message -->
    <div class="mb-6 rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
      <h3 class="text-xl font-semibold text-black dark:text-white mb-2">
        خوش آمدید {{ authStore.user?.first_name || 'کاربر گرامی' }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400">
        سیستم مدیریت یراقالات ناصری - آمار و گزارش‌های امروز
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-3 lg:grid-cols-4 xl:gap-6 2xl:gap-7.5 mb-6 max-w-7xl">
      <!-- Today Sales Card -->
      <InventoryCard
        :value="todayStats.totalSales"
        label="فروش امروز"
        type="success"
      />

      <!-- Total Products Card -->
      <InventoryCard
        :value="todayStats.totalProducts"
        label="کل محصولات"
        type="total"
      />

      <!-- Low Stock Card -->
      <InventoryCard
        :value="todayStats.lowStockItems"
        label="موجودی کم"
        type="warning"
      />

      <!-- Customers Card -->
      <InventoryCard
        :value="todayStats.totalCustomers"
        label="مشتریان"
        type="total"
      />
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4 2xl:gap-7.5 mb-6">
      <router-link
        to="/products/create"
        class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <div class="flex items-center gap-4">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-primary/10">
            <svg class="fill-primary" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 4V16M4 10H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-semibold text-black dark:text-white">افزودن محصول</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">محصول جدید اضافه کنید</p>
          </div>
        </div>
      </router-link>

      <router-link
        to="/sales"
        class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <div class="flex items-center gap-4">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-success/10">
            <svg class="fill-success" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7 9L10 12L17 5M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-semibold text-black dark:text-white">فروش/مشتریان</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">ثبت فروش/مشتری جدید</p>
          </div>
        </div>
      </router-link>

      <router-link
        to="/inventory"
        class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <div class="flex items-center gap-4">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-orange-500/10">
            <svg class="fill-orange-500" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M4 7V4C4 2.89543 4.89543 2 6 2H14C15.1046 2 16 2.89543 16 4V7M4 7H16M4 7L5 17C5 18.1046 5.89543 19 7 19H13C14.1046 19 15 18.1046 15 17L16 7" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-semibold text-black dark:text-white">مدیریت موجودی</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">بررسی موجودی انبار</p>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Recent Activities -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black dark:text-white">
          آخرین فعالیت‌ها
        </h4>
      </div>

      <div class="p-4 md:p-6 xl:p-7.5">
        <div class="space-y-4">
          <div v-for="activity in recentActivities" :key="activity.id" class="flex items-center gap-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
            <div class="flex h-10 w-10 items-center justify-center rounded-full" :class="activity.iconBg">
              <svg class="h-5 w-5" :class="activity.iconColor" fill="currentColor" viewBox="0 0 20 20">
                <path v-html="activity.icon"></path>
              </svg>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-black dark:text-white">{{ activity.title }}</p>
              <p class="text-xs text-gray-600 dark:text-gray-400">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </admin-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useProductsStore } from '@/stores/products'
import { useSalesStore } from '@/stores/sales'
import { useInventoryStore } from '@/stores/inventory'
import AdminLayout from '../components/layout/AdminLayout.vue'
import InventoryCard from '@/components/common/InventoryCard.vue'

const authStore = useAuthStore()
const productsStore = useProductsStore()
const salesStore = useSalesStore()
const inventoryStore = useInventoryStore()

// Dashboard stats - using mock data for now since backend might not be running
const todayStats = ref({
  totalSales: 2500000,
  totalProducts: 156,
  lowStockItems: 12,
  totalCustomers: 89
})

// Recent activities
const recentActivities = ref([
  {
    id: 1,
    title: 'محصول جدید "پیچ فلزی 8mm" اضافه شد',
    time: '5 دقیقه پیش',
    icon: 'M12 6v6m0 0v6m0-6h6m-6 0H6',
    iconBg: 'bg-primary/10',
    iconColor: 'text-primary'
  },
  {
    id: 2,
    title: 'فروش جدید به مشتری احمد محمدی',
    time: '15 دقیقه پیش',
    icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    iconBg: 'bg-success/10',
    iconColor: 'text-success'
  },
  {
    id: 3,
    title: 'هشدار: موجودی "مهره فلزی 6mm" کم است',
    time: '30 دقیقه پیش',
    icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    iconBg: 'bg-warning/10',
    iconColor: 'text-warning'
  }
])

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const loadDashboardData = async () => {
  try {
    // Try to load real data, but use mock data if backend is not available
    const results = await Promise.allSettled([
      productsStore.fetchProducts({ page_size: 1 }),
      salesStore.fetchCustomers({ page_size: 1 }),
      inventoryStore.fetchStockLevels()
    ])

    // Update stats with real data if available, otherwise keep mock data
    if (results.some(result => result.status === 'fulfilled')) {
      todayStats.value = {
        totalSales: salesStore.totalRevenue || todayStats.value.totalSales,
        totalProducts: productsStore.totalProducts || todayStats.value.totalProducts,
        lowStockItems: inventoryStore.lowStockProducts || todayStats.value.lowStockItems,
        totalCustomers: salesStore.totalCustomers || todayStats.value.totalCustomers
      }
    }
  } catch (error) {
    console.log('Using mock data - backend not available:', error)
  }
}

// Lifecycle
onMounted(() => {
  loadDashboardData()
})
</script>
