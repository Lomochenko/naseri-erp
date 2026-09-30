<template>
  <AdminLayout>
    <main class="mx-auto max-w-3xl" dir="rtl">
      <h1 class="mb-5 text-2xl font-bold text-gray-900 dark:text-white">پروفایل کاربری</h1>
      <section class="rounded-xl border border-amber-300 bg-white p-6 shadow-sm dark:border-amber-700 dark:bg-boxdark sm:p-8" role="status">
        <span class="inline-flex rounded-md bg-amber-100 px-2 py-1 text-xs font-bold text-amber-900 dark:bg-amber-900/50 dark:text-amber-100">به‌زودی</span>
        <h2 class="mt-4 text-xl font-semibold text-gray-900 dark:text-white">پروفایل در حال آماده‌سازی است</h2>
        <p class="mt-2 text-sm leading-7 text-gray-600 dark:text-gray-300">نمایش اطلاعات حساب، ویرایش مشخصات و اطلاعات پرداخت کارکنان در این صفحه هنوز به داده‌های واقعی متصل نیست. در حال حاضر تغییری از اینجا ذخیره نمی‌شود.</p>
        <router-link to="/" class="mt-6 inline-flex min-h-11 items-center rounded-lg bg-[#246b67] px-4 py-2 text-sm font-medium text-white hover:bg-[#1d5552] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#246b67]">بازگشت به داشبورد</router-link>
      </section>
    </main>
  </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layout/AdminLayout.vue'
</script>
