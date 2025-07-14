<template>
  <div class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
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
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16" fill="none">
            <path d="M11 15.1156C4.19376 15.1156 0.825012 8.61876 0.687512 8.34376C0.584387 8.13751 0.584387 7.86251 0.687512 7.65626C0.825012 7.38126 4.19376 0.918762 11 0.918762C17.8063 0.918762 21.175 7.38126 21.3125 7.65626C21.4156 7.86251 21.4156 8.13751 21.3125 8.34376C21.175 8.61876 17.8063 15.1156 11 15.1156ZM2.26876 8.00001C3.02501 9.27189 5.98126 13.5688 11 13.5688C16.0188 13.5688 18.975 9.27189 19.7313 8.00001C18.975 6.72814 16.0188 2.43126 11 2.43126C5.98126 2.43126 3.02501 6.72814 2.26876 8.00001Z"/>
            <path d="M11 10.9219C9.38438 10.9219 8.07812 9.61562 8.07812 8C8.07812 6.38438 9.38438 5.07812 11 5.07812C12.6156 5.07812 13.9219 6.38438 13.9219 8C13.9219 9.61562 12.6156 10.9219 11 10.9219ZM11 6.625C10.2437 6.625 9.625 7.24375 9.625 8C9.625 8.75625 10.2437 9.375 11 9.375C11.7563 9.375 12.375 8.75625 12.375 8C12.375 7.24375 11.7563 6.625 11 6.625Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ totalSales }}
            </h4>
            <span class="text-sm font-medium">کل فروش امروز</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
            <path d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312ZM11.7531 12.8687C11.1375 12.8687 10.6656 13.3406 10.6656 13.9562C10.6656 14.5719 11.1375 15.0437 11.7531 15.0437C12.3687 15.0437 12.8406 14.5719 12.8406 13.9562C12.8406 13.3406 12.3687 12.8687 11.7531 12.8687Z"/>
            <path d="M11.7531 7.84374C10.3781 7.84374 9.27808 6.74374 9.27808 5.36874C9.27808 3.99374 10.3781 2.89374 11.7531 2.89374C13.1281 2.89374 14.2281 3.99374 14.2281 5.36874C14.2281 6.74374 13.1281 7.84374 11.7531 7.84374ZM11.7531 4.28124C11.1375 4.28124 10.6656 4.75312 10.6656 5.36874C10.6656 5.98437 11.1375 6.45624 11.7531 6.45624C12.3687 6.45624 12.8406 5.98437 12.8406 5.36874C12.8406 4.75312 12.3687 4.28124 11.7531 4.28124Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ formatPrice(totalRevenue) }}
            </h4>
            <span class="text-sm font-medium">درآمد امروز</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M21.1063 18.0469L19.3875 3.23126C19.2157 1.71876 17.9438 0.584381 16.3969 0.584381H5.56878C4.05628 0.584381 2.78441 1.71876 2.57816 3.23126L0.859406 18.0469C0.756281 18.9063 1.03128 19.7313 1.61566 20.3844C2.20003 21.0375 2.99066 21.3813 3.85003 21.3813H18.1157C18.975 21.3813 19.8 21.0031 20.35 20.3844C20.9 19.7656 21.2094 18.9063 21.1063 18.0469ZM19.2157 19.3531C18.9407 19.6625 18.5625 19.8344 18.15 19.8344H3.85003C3.43753 19.8344 3.05941 19.6625 2.78441 19.3531C2.50941 19.0438 2.37191 18.6313 2.44066 18.2188L4.12503 3.43751C4.19378 2.71563 4.81253 2.16563 5.56878 2.16563H16.4313C17.1875 2.16563 17.8063 2.71563 17.875 3.43751L19.5938 18.2531C19.6282 18.6656 19.4907 19.0438 19.2157 19.3531Z"/>
            <path d="M14.3345 5.29375C13.922 5.39688 13.647 5.80938 13.7501 6.22188C13.7845 6.42813 13.8189 6.63438 13.8189 6.80625C13.8189 8.35313 12.547 9.625 11.0001 9.625C9.45327 9.625 8.18140 8.35313 8.18140 6.80625C8.18140 6.6 8.18140 6.42813 8.25015 6.22188C8.35327 5.80938 8.07827 5.39688 7.66577 5.29375C7.25327 5.19063 6.84077 5.46563 6.73765 5.87813C6.6689 6.1875 6.63452 6.49688 6.63452 6.80625C6.63452 9.2125 8.59390 11.1719 11.0001 11.1719C13.4064 11.1719 15.3658 9.2125 15.3658 6.80625C15.3658 6.49688 15.3314 6.1875 15.2626 5.87813C15.1595 5.46563 14.747 5.225 14.3345 5.29375Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ totalCustomers }}
            </h4>
            <span class="text-sm font-medium">مشتریان فعال</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-primary dark:fill-white" width="22" height="18" viewBox="0 0 22 18" fill="none">
            <path d="M7.18418 8.03751C9.31543 8.03751 11.0686 6.35313 11.0686 4.25626C11.0686 2.15938 9.31543 0.475006 7.18418 0.475006C5.05293 0.475006 3.2998 2.15938 3.2998 4.25626C3.2998 6.35313 5.05293 8.03751 7.18418 8.03751ZM7.18418 2.05626C8.45605 2.05626 9.52168 3.05313 9.52168 4.29063C9.52168 5.52813 8.49043 6.52501 7.18418 6.52501C5.87793 6.52501 4.84668 5.52813 4.84668 4.29063C4.84668 3.05313 5.9123 2.05626 7.18418 2.05626Z"/>
            <path d="M15.8124 9.6875C17.6687 9.6875 19.1468 8.24375 19.1468 6.42188C19.1468 4.6 17.6343 3.15625 15.8124 3.15625C13.9905 3.15625 12.478 4.6 12.478 6.42188C12.478 8.24375 13.9905 9.6875 15.8124 9.6875ZM15.8124 4.7375C16.8093 4.7375 17.5999 5.49375 17.5999 6.45625C17.5999 7.41875 16.8093 8.175 15.8124 8.175C14.8155 8.175 14.0249 7.41875 14.0249 6.45625C14.0249 5.49375 14.8155 4.7375 15.8124 4.7375Z"/>
            <path d="M15.9843 10.0313H15.6749C14.6437 10.0313 13.6468 10.3406 12.7781 10.8563C11.8593 9.61876 10.3812 8.79376 8.73115 8.79376H5.67178C2.85303 8.82814 0.618652 11.0625 0.618652 13.8469V16.3219C0.618652 17.0406 1.23740 17.625 1.95615 17.625H12.7468C13.4656 17.625 14.0843 17.0063 14.0843 16.2875V15.4188C14.0843 14.6313 14.2218 13.8781 14.4968 13.1594C14.9437 11.8563 16.1562 10.9375 17.5687 10.9375C17.9156 10.9375 18.2281 10.6594 18.2281 10.3125C18.2281 10.1406 18.1593 9.96876 18.0218 9.86564C17.8843 9.76251 17.7124 9.69376 17.5405 9.69376L15.9843 10.0313ZM2.16553 15.9844V13.8469C2.16553 11.9219 3.74678 10.3406 5.67178 10.3406H8.73115C10.6562 10.3406 12.2374 11.9219 12.2374 13.8469V15.9844H2.16553Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ pendingOrders }}
            </h4>
            <span class="text-sm font-medium">سفارشات در انتظار</span>
          </div>
        </div>
      </div>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'

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
