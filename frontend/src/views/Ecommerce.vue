<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        {{ brand.dashboardName }}
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
        {{ brand.businessName }}
      </p>
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

  </admin-layout>
</template>

<script setup>
import { brand } from '@/config/brand'
import { useAuthStore } from '@/stores/auth'
import AdminLayout from '../components/layout/AdminLayout.vue'

const authStore = useAuthStore()
</script>
