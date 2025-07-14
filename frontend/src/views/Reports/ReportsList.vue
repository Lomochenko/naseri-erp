<template>
  <AdminLayout>
    <div>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        گزارشات
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li>
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li class="font-medium text-primary">گزارشات</li>
        </ol>
      </nav>
    </div>

    <!-- Report Categories -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3 2xl:gap-7.5">
      <!-- Sales Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات فروش
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              گزارش‌های مربوط به فروش و درآمد
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16" fill="none">
              <path d="M11 15.1156C4.19376 15.1156 0.825012 8.61876 0.687512 8.34376C0.584387 8.13751 0.584387 7.86251 0.687512 7.65626C0.825012 7.38126 4.19376 0.918762 11 0.918762C17.8063 0.918762 21.175 7.38126 21.3125 7.65626C21.4156 7.86251 21.4156 8.13751 21.3125 8.34376C21.175 8.61876 17.8063 15.1156 11 15.1156Z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="generateReport('daily-sales')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش فروش روزانه
          </button>
          <button
            @click="generateReport('monthly-sales')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش فروش ماهانه
          </button>
          <button
            @click="generateReport('customer-sales')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش فروش به تفکیک مشتری
          </button>
          <button
            @click="generateReport('product-sales')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش فروش به تفکیک محصول
          </button>
        </div>
      </div>

      <!-- Inventory Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات موجودی
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              گزارش‌های مربوط به موجودی و انبار
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
              <path d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312Z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="generateReport('current-stock')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش موجودی فعلی
          </button>
          <button
            @click="generateReport('low-stock')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش موجودی کم
          </button>
          <button
            @click="generateReport('stock-movements')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش تحرکات موجودی
          </button>
          <button
            @click="generateReport('stock-valuation')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش ارزش‌گذاری موجودی
          </button>
        </div>
      </div>

      <!-- Financial Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات مالی
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              گزارش‌های مالی و حسابداری
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="22" height="22" viewBox="0 0 22 22" fill="none">
              <path d="M21.1063 18.0469L19.3875 3.23126C19.2157 1.71876 17.9438 0.584381 16.3969 0.584381H5.56878C4.05628 0.584381 2.78441 1.71876 2.57816 3.23126L0.859406 18.0469C0.756281 18.9063 1.03128 19.7313 1.61566 20.3844C2.20003 21.0375 2.99066 21.3813 3.85003 21.3813H18.1157C18.975 21.3813 19.8 21.0031 20.35 20.3844C20.9 19.7656 21.2094 18.9063 21.1063 18.0469Z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="generateReport('profit-loss')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش سود و زیان
          </button>
          <button
            @click="generateReport('balance-sheet')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            ترازنامه
          </button>
          <button
            @click="generateReport('cash-flow')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش جریان نقدی
          </button>
          <button
            @click="generateReport('accounts-receivable')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش حساب‌های دریافتنی
          </button>
        </div>
      </div>

      <!-- Purchase Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات خرید
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              گزارش‌های مربوط به خرید و تأمین‌کنندگان
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="22" height="18" viewBox="0 0 22 18" fill="none">
              <path d="M7.18418 8.03751C9.31543 8.03751 11.0686 6.35313 11.0686 4.25626C11.0686 2.15938 9.31543 0.475006 7.18418 0.475006C5.05293 0.475006 3.2998 2.15938 3.2998 4.25626C3.2998 6.35313 5.05293 8.03751 7.18418 8.03751Z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="generateReport('purchase-summary')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            خلاصه خریدها
          </button>
          <button
            @click="generateReport('supplier-performance')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            عملکرد تأمین‌کنندگان
          </button>
          <button
            @click="generateReport('purchase-orders')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش سفارشات خرید
          </button>
          <button
            @click="generateReport('accounts-payable')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش حساب‌های پرداختنی
          </button>
        </div>
      </div>

      <!-- Customer Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات مشتریان
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              گزارش‌های مربوط به مشتریان
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="18" height="18" viewBox="0 0 18 18" fill="none">
              <path d="M6.10322 0.956299C2.89135 0.956299 0.272217 3.57543 0.272217 6.78731C0.272217 10.0592 2.89135 12.6783 6.10322 12.6783C9.31509 12.6783 11.9342 10.0592 11.9342 6.78731C11.9342 3.57543 9.31509 0.956299 6.10322 0.956299Z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="generateReport('customer-list')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            لیست مشتریان
          </button>
          <button
            @click="generateReport('customer-activity')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            فعالیت مشتریان
          </button>
          <button
            @click="generateReport('top-customers')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            برترین مشتریان
          </button>
          <button
            @click="generateReport('customer-debts')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            بدهی مشتریان
          </button>
        </div>
      </div>

      <!-- Custom Reports -->
      <div class="rounded-sm border border-stroke bg-white p-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-title-md font-semibold text-black dark:text-white">
              گزارشات سفارشی
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              ایجاد گزارش‌های سفارشی
            </p>
          </div>
          <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="fill-primary dark:fill-white" width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zM9 5h2v2H9V5zm0 4h2v6H9V9z"/>
            </svg>
          </div>
        </div>

        <div class="mt-6 space-y-3">
          <button
            @click="showCustomReportModal = true"
            class="w-full rounded-lg bg-primary px-4 py-3 text-center text-sm text-white hover:bg-opacity-90"
          >
            ایجاد گزارش سفارشی
          </button>
          <button
            @click="generateReport('saved-reports')"
            class="w-full rounded-lg border border-stroke bg-transparent px-4 py-3 text-left text-sm text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
          >
            گزارش‌های ذخیره شده
          </button>
        </div>
      </div>
    </div>

    <!-- Recent Reports -->
    <div class="mt-8 rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black dark:text-white">
          آخرین گزارش‌های تولید شده
        </h4>
      </div>

      <div class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-3 flex items-center">
          <p class="font-medium">نام گزارش</p>
        </div>
        <div class="col-span-2 hidden items-center sm:flex">
          <p class="font-medium">تاریخ تولید</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">نوع</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">وضعیت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">عملیات</p>
        </div>
      </div>

      <!-- Sample Recent Reports -->
      <div v-for="report in recentReports" :key="report.id" class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-3 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ report.name }}</p>
        </div>
        <div class="col-span-2 hidden items-center sm:flex">
          <p class="text-sm text-black dark:text-white">{{ report.date }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ report.type }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <span
            :class="report.status === 'ready' ? 'bg-success text-success' : 'bg-warning text-warning'"
            class="inline-flex rounded-full bg-opacity-10 px-3 py-1 text-sm font-medium"
          >
            {{ report.status === 'ready' ? 'آماده' : 'در حال پردازش' }}
          </span>
        </div>
        <div class="col-span-1 flex items-center space-x-2">
          <button
            v-if="report.status === 'ready'"
            @click="downloadReport(report)"
            class="hover:text-primary"
            title="دانلود"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m-6 4h8" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Custom Report Modal -->
    <div v-if="showCustomReportModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-full max-w-lg rounded-lg bg-white p-6 dark:bg-boxdark">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-medium text-black dark:text-white">
            ایجاد گزارش سفارشی
          </h3>
          <button
            @click="showCustomReportModal = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="createCustomReport">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              نام گزارش
            </label>
            <input
              v-model="customReportForm.name"
              type="text"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="نام گزارش را وارد کنید"
            />
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              نوع گزارش
            </label>
            <select
              v-model="customReportForm.type"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
            >
              <option value="">نوع گزارش را انتخاب کنید</option>
              <option value="sales">فروش</option>
              <option value="inventory">موجودی</option>
              <option value="financial">مالی</option>
              <option value="customer">مشتری</option>
            </select>
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              بازه زمانی
            </label>
            <div class="grid grid-cols-2 gap-3">
              <input
                v-model="customReportForm.startDate"
                type="date"
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              />
              <input
                v-model="customReportForm.endDate"
                type="date"
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              />
            </div>
          </div>

          <div class="flex gap-3">
            <button
              type="submit"
              class="flex-1 rounded bg-primary px-4 py-2 text-white hover:bg-opacity-90"
            >
              تولید گزارش
            </button>
            <button
              type="button"
              @click="showCustomReportModal = false"
              class="flex-1 rounded border border-stroke px-4 py-2 text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
            >
              انصراف
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'

// Reactive data
const showCustomReportModal = ref(false)

const customReportForm = ref({
  name: '',
  type: '',
  startDate: '',
  endDate: ''
})

// Sample recent reports
const recentReports = ref([
  {
    id: 1,
    name: 'گزارش فروش روزانه',
    date: '1403/01/15',
    type: 'فروش',
    status: 'ready'
  },
  {
    id: 2,
    name: 'گزارش موجودی کم',
    date: '1403/01/14',
    type: 'موجودی',
    status: 'ready'
  },
  {
    id: 3,
    name: 'گزارش سود و زیان ماهانه',
    date: '1403/01/13',
    type: 'مالی',
    status: 'processing'
  }
])

// Methods
const generateReport = (reportType) => {
  console.log('Generating report:', reportType)
  // Here you would call the appropriate API endpoint
}

const downloadReport = (report) => {
  console.log('Downloading report:', report)
  // Here you would download the report file
}

const createCustomReport = () => {
  console.log('Creating custom report:', customReportForm.value)
  showCustomReportModal.value = false
  customReportForm.value = {
    name: '',
    type: '',
    startDate: '',
    endDate: ''
  }
}
</script>
