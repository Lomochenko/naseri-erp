<template>
  <AdminLayout>
    <div>
      <!-- Breadcrumb -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h2 class="text-title-md2 font-bold text-black dark:text-white">
          مدیریت فروش
        </h2>
        <nav>
          <ol class="flex items-center gap-2">
            <li>
              <router-link class="font-medium text-black dark:text-white" to="/">داشبورد /</router-link>
            </li>
            <li class="font-medium text-black dark:text-white">فروش</li>
          </ol>
        </nav>
      </div>

      <!-- Sales Stats -->
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
        <!-- Today Sales -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16" fill="none">
              <path d="M11 15.1156C4.19376 15.1156 0.825012 8.61876 0.687512 8.34376C0.584387 8.13751 0.584387 7.86251 0.687512 7.65626C0.825012 7.38126 4.19376 0.918762 11 0.918762C17.8063 0.918762 21.175 7.38126 21.3125 7.65626C21.4156 7.86251 21.4156 8.13751 21.3125 8.34376C21.175 8.61876 17.8063 15.1156 11 15.1156ZM2.26876 8.00001C3.02501 9.27189 5.98126 13.5688 11 13.5688C16.0188 13.5688 18.975 9.27189 19.7313 8.00001C18.975 6.72814 16.0188 2.43126 11 2.43126C5.98126 2.43126 3.02501 6.72814 2.26876 8.00001Z"/>
              <path d="M11 10.9219C9.38438 10.9219 8.07812 9.61562 8.07812 8C8.07812 6.38438 9.38438 5.07812 11 5.07812C12.6156 5.07812 13.9219 6.38438 13.9219 8C13.9219 9.61562 12.6156 10.9219 11 10.9219ZM11 6.625C10.2437 6.625 9.625 7.24375 9.625 8C9.625 8.75625 10.2437 9.375 11 9.375C11.7563 9.375 12.375 8.75625 12.375 8C12.375 7.24375 11.7563 6.625 11 6.625Z"/>
            </svg>
          </div>
          <div class="mt-4 flex items-end justify-between">
            <div>
              <h4 class="text-title-md font-bold text-black dark:text-white">
                {{ formatPrice(salesStats.todaySales) }}
              </h4>
              <span class="text-sm font-medium">فروش امروز</span>
            </div>
          </div>
        </div>

        <!-- This Month Sales -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312ZM11.7531 12.8687C11.2375 12.8687 10.8281 13.2781 10.8281 13.7937C10.8281 14.3094 11.2375 14.7187 11.7531 14.7187C12.2688 14.7187 12.6781 14.3094 12.6781 13.7937C12.6781 13.2781 12.2688 12.8687 11.7531 12.8687Z"/>
              <path d="M11.7531 7.84374C10.3781 7.84374 9.27808 6.74374 9.27808 5.36874C9.27808 3.99374 10.3781 2.89374 11.7531 2.89374C13.1281 2.89374 14.2281 3.99374 14.2281 5.36874C14.2281 6.74374 13.1281 7.84374 11.7531 7.84374ZM11.7531 4.28124C11.2375 4.28124 10.8281 4.69061 10.8281 5.20624C10.8281 5.72186 11.2375 6.13124 11.7531 6.13124C12.2688 6.13124 12.6781 5.72186 12.6781 5.20624C12.6781 4.69061 12.2688 4.28124 11.7531 4.28124Z"/>
            </svg>
          </div>
          <div class="mt-4 flex items-end justify-between">
            <div>
              <h4 class="text-title-md font-bold text-black dark:text-white">
                {{ formatPrice(salesStats.monthSales) }}
              </h4>
              <span class="text-sm font-medium">فروش این ماه</span>
            </div>
          </div>
        </div>

        <!-- Total Customers -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
            </svg>
          </div>
          <div class="mt-4 flex items-end justify-between">
            <div>
              <h4 class="text-title-md font-bold text-black dark:text-white">
                {{ salesStats.totalCustomers }}
              </h4>
              <span class="text-sm font-medium">تعداد مشتریان</span>
            </div>
          </div>
        </div>

        <!-- Pending Orders -->
        <div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
          </div>
          <div class="mt-4 flex items-end justify-between">
            <div>
              <h4 class="text-title-md font-bold text-black dark:text-white">
                {{ salesStats.pendingOrders }}
              </h4>
              <span class="text-sm font-medium">سفارشات در انتظار</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="-mb-px flex space-x-8 space-x-reverse">
            <button @click="activeTab = 'orders'"
              :class="activeTab === 'orders' ? 'border-primary text-black dark:text-white' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm">
              سفارشات فروش
            </button>
            <button @click="activeTab = 'customers'"
              :class="activeTab === 'customers' ? 'border-primary text-black dark:text-white' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm">
              مشتریان
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div v-if="activeTab === 'orders'">
        <SalesOrderList />
      </div>

      <div v-if="activeTab === 'customers'">
        <CustomerList />
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import SalesOrderList from '@/components/sales/SalesOrderList.vue'
import CustomerList from '@/components/sales/CustomerList.vue'

// Store
const salesStore = useSalesStore()

// State
const activeTab = ref('orders')

// Computed
const salesStats = computed(() => salesStore.stats || {
  todaySales: 0,
  monthSales: 0,
  totalCustomers: 0,
  pendingOrders: 0
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

// Lifecycle
onMounted(async () => {
  await salesStore.fetchStats()
})
</script>
