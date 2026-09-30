<template>
  <AdminLayout>
    <main class="mx-auto max-w-7xl space-y-6" dir="rtl">
      <header class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="mb-1 text-xs font-semibold text-[#246b67]">گزارش‌گیری</p>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">گزارش‌ها</h1>
        </div>
        <router-link to="/" class="text-sm font-medium text-[#246b67] underline-offset-4 hover:underline focus-visible:underline">بازگشت به داشبورد</router-link>
      </header>

      <section class="rounded-xl border border-amber-300 bg-amber-50 px-5 py-4 text-amber-950 dark:border-amber-700 dark:bg-amber-950/30 dark:text-amber-100" role="status" aria-label="وضعیت گزارش‌گیری">
        <div class="flex flex-wrap items-center gap-2">
          <span class="rounded-md bg-amber-200 px-2 py-0.5 text-xs font-bold text-amber-950 dark:bg-amber-800 dark:text-white">به‌زودی</span>
          <h2 class="font-semibold">گزارش‌گیری هنوز فعال نیست</h2>
        </div>
        <p class="mt-2 text-sm leading-7">در این نسخه هیچ‌یک از گزینه‌های زیر فایل گزارش تولید یا ذخیره نمی‌کنند. برای تصمیم‌های مالی به این صفحه اتکا نکنید؛ بخش‌های عملیاتی از منوی اصلی در دسترس‌اند.</p>
      </section>

      <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        <section v-for="category in categories" :key="category.title" class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-boxdark" :aria-label="category.title">
          <div class="mb-4 flex items-start justify-between gap-3 border-b border-gray-100 pb-4 dark:border-gray-700">
            <div>
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{{ category.title }}</h2>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-300">{{ category.description }}</p>
            </div>
            <span class="shrink-0 rounded-md bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-900 dark:bg-amber-900/50 dark:text-amber-100">به‌زودی</span>
          </div>
          <ul class="space-y-2">
            <li v-for="item in category.items" :key="item" class="flex min-h-11 items-center justify-between gap-3 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200">
              <span>{{ item }}</span>
              <span class="shrink-0 text-xs font-medium text-amber-800 dark:text-amber-200">غیرفعال</span>
            </li>
          </ul>
        </section>
      </div>

      <section class="rounded-xl border border-gray-200 bg-white px-5 py-5 dark:border-gray-700 dark:bg-boxdark">
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">گزارش‌های سفارشی و ذخیره‌شده</h2>
          <span class="rounded-md bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-900 dark:bg-amber-900/50 dark:text-amber-100">به‌زودی</span>
        </div>
        <p class="mt-2 text-sm leading-7 text-gray-600 dark:text-gray-300">ساخت، ذخیره و دانلود گزارش سفارشی هنوز پیاده‌سازی نشده است. گزارشی در این بخش تولید نمی‌شود.</p>
      </section>
    </main>
  </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layout/AdminLayout.vue'

const categories = [
  { title: 'فروش', description: 'آمار فروش و درآمد', items: ['فروش روزانه', 'فروش ماهانه', 'فروش به تفکیک مشتری', 'فروش به تفکیک محصول'] },
  { title: 'موجودی', description: 'تحلیل موجودی و انبار', items: ['موجودی فعلی', 'موجودی کم', 'تحرکات موجودی', 'ارزش‌گذاری موجودی'] },
  { title: 'مالی', description: 'صورت‌ها و حساب‌های مالی', items: ['سود و زیان', 'ترازنامه', 'جریان نقدی', 'حساب‌های دریافتنی'] },
  { title: 'خرید', description: 'خریدها و تأمین‌کنندگان', items: ['خلاصه خریدها', 'عملکرد تأمین‌کنندگان', 'سفارش‌های خرید', 'حساب‌های پرداختنی'] },
  { title: 'مشتریان', description: 'تحلیل مشتریان', items: ['فهرست مشتریان', 'فعالیت مشتریان', 'برترین مشتریان', 'بدهی مشتریان'] },
]
</script>
