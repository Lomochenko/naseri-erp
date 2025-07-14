<template>
  <div class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        مدیریت موجودی
      </h2>
      <nav>
        <ol class="flex items-center gap-2">
          <li>
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li class="font-medium text-primary">موجودی</li>
        </ol>
      </nav>
    </div>

    <!-- Action Buttons -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex gap-3">
        <button
          @click="showAdjustmentModal = true"
          class="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-center font-medium text-white hover:bg-opacity-90"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          تعدیل موجودی
        </button>
        
        <button
          @click="showTransactionModal = true"
          class="inline-flex items-center justify-center rounded-md border border-primary px-6 py-3 text-center font-medium text-primary hover:bg-opacity-90"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>
          انتقال موجودی
        </button>
      </div>
      
      <!-- Search -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در موجودی..."
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
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-black dark:text-white">
              {{ totalProducts }}
            </h4>
            <span class="text-sm font-medium">کل محصولات</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-success dark:fill-white" width="20" height="22" viewBox="0 0 20 22" fill="none">
            <path d="M11.7531 16.4312C10.3781 16.4312 9.27808 15.3312 9.27808 13.9562C9.27808 12.5812 10.3781 11.4812 11.7531 11.4812C13.1281 11.4812 14.2281 12.5812 14.2281 13.9562C14.2281 15.3312 13.1281 16.4312 11.7531 16.4312Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-success dark:text-white">
              {{ inStockProducts }}
            </h4>
            <span class="text-sm font-medium">محصولات موجود</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-warning dark:fill-white" width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M21.1063 18.0469L19.3875 3.23126C19.2157 1.71876 17.9438 0.584381 16.3969 0.584381H5.56878C4.05628 0.584381 2.78441 1.71876 2.57816 3.23126L0.859406 18.0469C0.756281 18.9063 1.03128 19.7313 1.61566 20.3844C2.20003 21.0375 2.99066 21.3813 3.85003 21.3813H18.1157C18.975 21.3813 19.8 21.0031 20.35 20.3844C20.9 19.7656 21.2094 18.9063 21.1063 18.0469Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-warning dark:text-white">
              {{ lowStockProducts }}
            </h4>
            <span class="text-sm font-medium">موجودی کم</span>
          </div>
        </div>
      </div>

      <div class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
          <svg class="fill-danger dark:fill-white" width="22" height="18" viewBox="0 0 22 18" fill="none">
            <path d="M7.18418 8.03751C9.31543 8.03751 11.0686 6.35313 11.0686 4.25626C11.0686 2.15938 9.31543 0.475006 7.18418 0.475006C5.05293 0.475006 3.2998 2.15938 3.2998 4.25626C3.2998 6.35313 5.05293 8.03751 7.18418 8.03751Z"/>
          </svg>
        </div>
        <div class="mt-4 flex items-end justify-between">
          <div>
            <h4 class="text-title-md font-bold text-danger dark:text-white">
              {{ outOfStockProducts }}
            </h4>
            <span class="text-sm font-medium">ناموجود</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Inventory Table -->
    <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black dark:text-white">
          وضعیت موجودی محصولات
        </h4>
      </div>

      <div class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <p class="font-medium">نام محصول</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="font-medium">دسته‌بندی</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">موجودی فعلی</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">حداقل</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">حداکثر</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">وضعیت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">عملیات</p>
        </div>
      </div>

      <!-- Sample Inventory Data -->
      <div v-for="item in sampleInventory" :key="item.id" class="grid grid-cols-6 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ item.productName }}</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="text-sm text-black dark:text-white">{{ item.category }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm font-medium" :class="getStockClass(item.currentStock, item.minStock)">
            {{ item.currentStock }}
          </p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ item.minStock }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black dark:text-white">{{ item.maxStock }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <span
            :class="getStatusClass(item.currentStock, item.minStock)"
            class="inline-flex rounded-full bg-opacity-10 px-3 py-1 text-sm font-medium"
          >
            {{ getStatusText(item.currentStock, item.minStock) }}
          </span>
        </div>
        <div class="col-span-1 flex items-center space-x-2">
          <button
            @click="adjustStock(item)"
            class="hover:text-primary"
            title="تعدیل موجودی"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            @click="viewHistory(item)"
            class="hover:text-primary ml-2"
            title="تاریخچه"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Stock Adjustment Modal -->
    <div v-if="showAdjustmentModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="w-full max-w-md rounded-lg bg-white p-6 dark:bg-boxdark">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-medium text-black dark:text-white">
            تعدیل موجودی
          </h3>
          <button
            @click="closeAdjustmentModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleAdjustment">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              محصول
            </label>
            <select
              v-model="adjustmentForm.productId"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
            >
              <option value="">محصول را انتخاب کنید</option>
              <option v-for="item in sampleInventory" :key="item.id" :value="item.id">
                {{ item.productName }} (موجودی فعلی: {{ item.currentStock }})
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              نوع تعدیل
            </label>
            <select
              v-model="adjustmentForm.type"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
            >
              <option value="">نوع تعدیل را انتخاب کنید</option>
              <option value="increase">افزایش موجودی</option>
              <option value="decrease">کاهش موجودی</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              مقدار
            </label>
            <input
              v-model="adjustmentForm.quantity"
              type="number"
              min="1"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="مقدار تعدیل"
            />
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-black dark:text-white">
              دلیل تعدیل
            </label>
            <textarea
              v-model="adjustmentForm.reason"
              rows="3"
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              placeholder="دلیل تعدیل موجودی"
            ></textarea>
          </div>

          <div class="flex gap-3">
            <button
              type="submit"
              class="flex-1 rounded bg-primary px-4 py-2 text-white hover:bg-opacity-90"
            >
              تعدیل موجودی
            </button>
            <button
              type="button"
              @click="closeAdjustmentModal"
              class="flex-1 rounded border border-stroke px-4 py-2 text-black hover:bg-gray-50 dark:border-strokedark dark:text-white dark:hover:bg-meta-4"
            >
              انصراف
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Reactive data
const searchQuery = ref('')
const showAdjustmentModal = ref(false)
const showTransactionModal = ref(false)

const adjustmentForm = ref({
  productId: '',
  type: '',
  quantity: '',
  reason: ''
})

// Sample stats
const totalProducts = ref(156)
const inStockProducts = ref(142)
const lowStockProducts = ref(12)
const outOfStockProducts = ref(2)

// Sample inventory data
const sampleInventory = ref([
  {
    id: 1,
    productName: 'پیچ فلزی 6mm',
    category: 'پیچ و مهره',
    currentStock: 250,
    minStock: 50,
    maxStock: 500
  },
  {
    id: 2,
    productName: 'مهره فلزی 6mm',
    category: 'پیچ و مهره',
    currentStock: 15,
    minStock: 30,
    maxStock: 300
  },
  {
    id: 3,
    productName: 'چکش 500 گرمی',
    category: 'ابزار',
    currentStock: 0,
    minStock: 5,
    maxStock: 50
  }
])

// Methods
const getStockClass = (current, min) => {
  if (current <= 0) return 'text-danger'
  if (current <= min) return 'text-warning'
  return 'text-success'
}

const getStatusClass = (current, min) => {
  if (current <= 0) return 'bg-danger text-danger'
  if (current <= min) return 'bg-warning text-warning'
  return 'bg-success text-success'
}

const getStatusText = (current, min) => {
  if (current <= 0) return 'ناموجود'
  if (current <= min) return 'موجودی کم'
  return 'موجود'
}

const adjustStock = (item) => {
  adjustmentForm.value.productId = item.id
  showAdjustmentModal.value = true
}

const viewHistory = (item) => {
  console.log('View history for:', item)
}

const closeAdjustmentModal = () => {
  showAdjustmentModal.value = false
  adjustmentForm.value = {
    productId: '',
    type: '',
    quantity: '',
    reason: ''
  }
}

const handleAdjustment = () => {
  // Handle stock adjustment
  console.log('Stock adjustment:', adjustmentForm.value)
  closeAdjustmentModal()
}
</script>
