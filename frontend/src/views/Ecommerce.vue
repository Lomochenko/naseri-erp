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
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
      <!-- Total Sales -->
      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16" fill="none">
            <path d="M11 15.1156C4.19376 15.1156 0.825012 8.61876 0.687512 8.34376C0.584387 8.13751 0.584387 7.86251 0.687512 7.65626C0.825012 7.38126 4.19376 0.918762 11 0.918762C17.8063 0.918762 21.175 7.38126 21.3125 7.65626C21.4156 7.86251 21.4156 8.13751 21.3125 8.34376C21.175 8.61876 17.8063 15.1156 11 15.1156Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ formatPrice(todayStats.totalSales) }}
            </h4>
            <span class="text-sm font-medium">فروش امروز</span>
          </div>
        </div>
      </div>

      <!-- Total Products -->
      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
            <path d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ todayStats.totalProducts }}
            </h4>
            <span class="text-sm font-medium">کل محصولات</span>
          </div>
        </div>
      </div>

      <!-- Low Stock -->
      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-warning dark:fill-white" width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M21.1063 18.0469L19.3875 3.23126C19.2157 1.71876 17.9438 0.584381 16.3969 0.584381H5.56878C4.05628 0.584381 2.78441 1.71876 2.57816 3.23126L0.859406 18.0469C0.756281 18.9063 1.03128 19.7313 1.61566 20.3844C2.20003 21.0375 2.99066 21.3813 3.85003 21.3813H18.1157C18.975 21.3813 19.8 21.0031 20.35 20.3844C20.9 19.7656 21.2094 18.9063 21.1063 18.0469Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-warning dark:text-white">
              {{ todayStats.lowStockItems }}
            </h4>
            <span class="text-sm font-medium">موجودی کم</span>
          </div>
        </div>
      </div>

      <!-- Total Customers -->
      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="22" height="18" viewBox="0 0 22 18" fill="none">
            <path d="M7.18418 8.03751C9.31543 8.03751 11.0686 6.35313 11.0686 4.25626C11.0686 2.15938 9.31543 0.475006 7.18418 0.475006C5.05293 0.475006 3.2998 2.15938 3.2998 4.25626C3.2998 6.35313 5.05293 8.03751 7.18418 8.03751Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ todayStats.totalCustomers }}
            </h4>
            <span class="text-sm font-medium">مشتریان</span>
          </div>
        </div>
      </div>
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
            <h4 class="text-lg font-semibold text-black dark:text-white">فروش جدید</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">ثبت فروش جدید</p>
          </div>
        </div>
      </router-link>

      <router-link
        to="/customers"
        class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <div class="flex items-center gap-4">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-blue-light-500/10">
            <svg class="fill-blue-light-500" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2"/>
              <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div>
            <h4 class="text-lg font-semibold text-black dark:text-white">مشتری جدید</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">افزودن مشتری جدید</p>
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
