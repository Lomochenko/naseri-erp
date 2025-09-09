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
        <div
          class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16" fill="none">
              <path
                d="M11 15.1156C4.19376 15.1156 0.825012 8.61876 0.687512 8.34376C0.584387 8.13751 0.584387 7.86251 0.687512 7.65626C0.825012 7.38126 4.19376 0.918762 11 0.918762C17.8063 0.918762 21.175 7.38126 21.3125 7.65626C21.4156 7.86251 21.4156 8.13751 21.3125 8.34376C21.175 8.61876 17.8063 15.1156 11 15.1156ZM2.26876 8.00001C3.02501 9.27189 5.98126 13.5688 11 13.5688C16.0188 13.5688 18.975 9.27189 19.7313 8.00001C18.975 6.72814 16.0188 2.43126 11 2.43126C5.98126 2.43126 3.02501 6.72814 2.26876 8.00001Z" />
              <path
                d="M11 10.9219C9.38438 10.9219 8.07812 9.61562 8.07812 8C8.07812 6.38438 9.38438 5.07812 11 5.07812C12.6156 5.07812 13.9219 6.38438 13.9219 8C13.9219 9.61562 12.6156 10.9219 11 10.9219ZM11 6.625C10.2437 6.625 9.625 7.24375 9.625 8C9.625 8.75625 10.2437 9.375 11 9.375C11.7563 9.375 12.375 8.75625 12.375 8C12.375 7.24375 11.7563 6.625 11 6.625Z" />
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
        <div
          class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path
                d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312ZM11.7531 12.8687C11.2375 12.8687 10.8281 13.2781 10.8281 13.7937C10.8281 14.3094 11.2375 14.7187 11.7531 14.7187C12.2688 14.7187 12.6781 14.3094 12.6781 13.7937C12.6781 13.2781 12.2688 12.8687 11.7531 12.8687Z" />
              <path
                d="M11.7531 7.84374C10.3781 7.84374 9.27808 6.74374 9.27808 5.36874C9.27808 3.99374 10.3781 2.89374 11.7531 2.89374C13.1281 2.89374 14.2281 3.99374 14.2281 5.36874C14.2281 6.74374 13.1281 7.84374 11.7531 7.84374ZM11.7531 4.28124C11.2375 4.28124 10.8281 4.69061 10.8281 5.20624C10.8281 5.72186 11.2375 6.13124 11.7531 6.13124C12.2688 6.13124 12.6781 5.72186 12.6781 5.20624C12.6781 4.69061 12.2688 4.28124 11.7531 4.28124Z" />
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
        <div
          class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path
                d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
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
        <div
          class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path
                d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
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

      <!-- Modern Tabs -->
      <div class="mb-6">
        <div class="bg-gray-100 dark:bg-gray-800 p-1 rounded-xl inline-flex">
          <button @click="activeTab = 'orders'" :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 flex items-center',
            activeTab === 'orders'
              ? 'bg-white dark:bg-gray-700 dark:text-white shadow-md'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
          ]">
            <svg class="ml-1" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd"
                d="M9.85954 4.0835C9.5834 4.0835 9.35954 4.30735 9.35954 4.5835V15.4161C9.35954 15.6922 9.5834 15.9161 9.85954 15.9161H10.1373C10.4135 15.9161 10.6373 15.6922 10.6373 15.4161V4.5835C10.6373 4.30735 10.4135 4.0835 10.1373 4.0835H9.85954ZM7.85954 4.5835C7.85954 3.47893 8.75497 2.5835 9.85954 2.5835H10.1373C11.2419 2.5835 12.1373 3.47893 12.1373 4.5835V15.4161C12.1373 16.5206 11.2419 17.4161 10.1373 17.4161H9.85954C8.75497 17.4161 7.85954 16.5206 7.85954 15.4161V4.5835ZM4.58203 8.9598C4.30589 8.9598 4.08203 9.18366 4.08203 9.4598V15.4168C4.08203 15.693 4.30589 15.9168 4.58203 15.9168H4.85981C5.13595 15.9168 5.35981 15.693 5.35981 15.4168V9.4598C5.35981 9.18366 5.13595 8.9598 4.85981 8.9598H4.58203ZM2.58203 9.4598C2.58203 8.35523 3.47746 7.4598 4.58203 7.4598H4.85981C5.96438 7.4598 6.85981 8.35523 6.85981 9.4598V15.4168C6.85981 16.5214 5.96438 17.4168 4.85981 17.4168H4.58203C3.47746 17.4168 2.58203 16.5214 2.58203 15.4168V9.4598ZM14.637 12.435C14.637 12.1589 14.8609 11.935 15.137 11.935H15.4148C15.691 11.935 15.9148 12.1589 15.9148 12.435V15.4168C15.9148 15.693 15.691 15.9168 15.4148 15.9168H15.137C14.8609 15.9168 14.637 15.693 14.637 15.4168V12.435ZM15.137 10.435C14.0325 10.435 13.137 11.3304 13.137 12.435V15.4168C13.137 16.5214 14.0325 17.4168 15.137 17.4168H15.4148C16.5194 17.4168 17.4148 16.5214 17.4148 15.4168V12.435C17.4148 11.3304 16.5194 10.435 15.4148 10.435H15.137Z"
                fill="currentColor" />
            </svg>
            سفارشات فروش
          </button>
          <button @click="activeTab = 'customers'" :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300 flex items-center',
            activeTab === 'customers'
              ? 'bg-white dark:bg-gray-700 dark:text-white shadow-md'
              : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
          ]">
            <svg class="ml-1" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" clip-rule="evenodd"
                d="M12 3.5C7.30558 3.5 3.5 7.30558 3.5 12C3.5 14.1526 4.3002 16.1184 5.61936 17.616C6.17279 15.3096 8.24852 13.5955 10.7246 13.5955H13.2746C15.7509 13.5955 17.8268 15.31 18.38 17.6167C19.6996 16.119 20.5 14.153 20.5 12C20.5 7.30558 16.6944 3.5 12 3.5ZM17.0246 18.8566V18.8455C17.0246 16.7744 15.3457 15.0955 13.2746 15.0955H10.7246C8.65354 15.0955 6.97461 16.7744 6.97461 18.8455V18.856C8.38223 19.8895 10.1198 20.5 12 20.5C13.8798 20.5 15.6171 19.8898 17.0246 18.8566ZM2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12ZM11.9991 7.25C10.8847 7.25 9.98126 8.15342 9.98126 9.26784C9.98126 10.3823 10.8847 11.2857 11.9991 11.2857C13.1135 11.2857 14.0169 10.3823 14.0169 9.26784C14.0169 8.15342 13.1135 7.25 11.9991 7.25ZM8.48126 9.26784C8.48126 7.32499 10.0563 5.75 11.9991 5.75C13.9419 5.75 15.5169 7.32499 15.5169 9.26784C15.5169 11.2107 13.9419 12.7857 11.9991 12.7857C10.0563 12.7857 8.48126 11.2107 8.48126 9.26784Z"
                fill="currentColor" />
            </svg>
            مشتریان
          </button>
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
