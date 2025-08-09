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
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li class="font-medium text-primary">فروش</li>
        </ol>
      </nav>
    </div>

    <!-- Action Buttons -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex gap-3">
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-center font-medium text-white hover:bg-opacity-90"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          فروش جدید
        </button>

        <router-link
          to="/customers"
          class="inline-flex items-center justify-center rounded-md border border-primary px-6 py-3 text-center font-medium text-primary hover:bg-opacity-90"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          مدیریت مشتریان
        </router-link>
      </div>

      <!-- Search -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در فروش..."
          class="w-full rounded-lg border border-stroke bg-transparent py-3 pl-12 pr-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
        />
        <svg
          class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-body"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-3 lg:grid-cols-4 xl:gap-6 2xl:gap-7.5 mb-6 max-w-7xl">
      <!-- Total Sales Today Card -->
      <InventoryCard
        :value="totalSales"
        label="کل فروش امروز"
        type="success"
      />
      
      <!-- Total Revenue Card -->
      <InventoryCard
        :value="totalRevenue"
        label="درآمد امروز"
        type="total"
      />
      
      <!-- Active Customers Card -->
      <InventoryCard
        :value="totalCustomers"
        label="مشتریان فعال"
        type="total"
      />
      
      <!-- Pending Orders Card -->
      <InventoryCard
        :value="pendingOrders"
        label="سفارشات در انتظار"
        type="warning"
      />
    </div>

    <!-- Sales Table -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black dark:text-white">
          آخرین فروش‌ها
        </h4>
      </div>

      <div class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-1 flex items-center">
          <p class="font-medium">شماره</p>
        </div>
        <div class="col-span-2 flex items-center">
          <p class="font-medium">مشتری</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="font-medium">تاریخ</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">مبلغ</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">وضعیت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">عملیات</p>
        </div>
      </div>

      <!-- Sample Data - Replace with real data -->
      <div class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">#001</p>
        </div>
        <div class="col-span-2 flex items-center">
          <p class="text-sm text-black dark:text-white">احمد محمدی</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="text-sm text-black dark:text-white">1403/01/15</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">2,500,000 تومان</p>
        </div>
        <div class="col-span-1 flex items-center">
          <span class="inline-flex rounded-full bg-success bg-opacity-10 px-3 py-1 text-sm font-medium text-success">
            تکمیل شده
          </span>
        </div>
        <div class="col-span-1 flex items-center space-x-2">
          <button class="hover:text-primary" title="مشاهده">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import InventoryCard from '@/components/common/InventoryCard.vue'

// Reactive data
const searchQuery = ref('')
const showCreateModal = ref(false)

// Sample stats - Replace with real data from store
const totalSales = ref(25)
const totalRevenue = ref(15750000)
const totalCustomers = ref(142)
const pendingOrders = ref(8)

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

// Lifecycle
onMounted(() => {
  // Load sales data
})
</script>
