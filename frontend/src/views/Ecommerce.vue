<template>
  <admin-layout>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        {{ brand.dashboardName }}
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li class="font-medium text-primary dark:text-brand-300">داشبورد اصلی</li>
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
    <div class="quick-actions grid grid-cols-1 gap-4 md:grid-cols-3 mb-6" aria-label="دسترسی سریع">
      <router-link
        to="/products/create"
        class="quick-action action-products"
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
        class="quick-action action-sales"
      >
        <div class="flex items-center gap-4">
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-success/10">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
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
        class="quick-action action-inventory"
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

<style scoped>
.quick-action { --action-color: #1d4ed8; --action-tint: #eff6ff; display: block; padding: 1.5rem; border: 1px solid color-mix(in srgb, var(--action-color) 25%, transparent); border-inline-start: 4px solid var(--action-color); border-radius: 14px; background: var(--action-tint); transition: transform 180ms ease, box-shadow 180ms ease; }
.action-sales { --action-color: #047857; --action-tint: #ecfdf5; }
.action-inventory { --action-color: #b45309; --action-tint: #fffbeb; }
.quick-action svg { color: var(--action-color); fill: none; }
.quick-action:hover { transform: translateY(-2px); box-shadow: 0 6px 18px #10182812; }
.quick-action:focus-visible { outline: 3px solid var(--action-color); outline-offset: 3px; }
:global(.dark .quick-action) { --action-tint: #1d2939; --action-color: #93c5fd; }
:global(.dark .action-sales) { --action-color: #6ee7b7; }
:global(.dark .action-inventory) { --action-color: #fcd34d; }
@media (prefers-reduced-motion: reduce) { .quick-action { transition: none; } .quick-action:hover { transform: none; } }
</style>
