<template>
  <AdminLayout>
    <div>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black">
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

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5 mb-6">
      <!-- Total Products Card -->
      <InventoryCard
        :value="inventoryStore.totalProducts"
        label="کل محصولات"
        type="total"
      />

      <!-- In Stock Products Card -->
      <InventoryCard
        :value="inventoryStore.inStockProducts"
        label="محصولات موجود"
        type="success"
      />

      <!-- Low Stock Products Card -->
      <InventoryCard
        :value="inventoryStore.lowStockProducts"
        label="موجودی کم"
        type="warning"
      />

      <!-- Out of Stock Products Card -->
      <InventoryCard
        :value="inventoryStore.outOfStockProducts"
        label="ناموجود"
        type="danger"
      />
    </div>
<!-- Action Buttons -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex gap-3">
        <button
          @click="showAdjustmentModal = true"
          class="inline-flex items-center justify-center rounded-md border-[1.5px] border-gray-200 bg-primary px-6 py-3 text-center font-medium text-dark dark:text-white"
        >
          <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          تعدیل موجودی
        </button>

        <button
          @click="showTransactionModal = true"
          class="inline-flex items-center justify-center rounded-md border-[1.5px] border-primary px-6 py-3 text-center font-medium text-dark dark:text-white hover:bg-opacity-90"
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
          class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 pl-12 pr-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
        />
        <svg
          class="absolute left-2 top-1/2 h-5 w-5 -translate-y-1/2 text-black dark:text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <!-- Inventory Table -->
    <div class="rounded-sm border border-stroke  bg-slate-100 dark:bg-slate-300  shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black">
          وضعیت موجودی محصولات
        </h4>
      </div>

      <div class="grid grid-cols-6 bg-slate-100 dark:bg-slate-300 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
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
      <div v-for="item in sampleInventory" :key="item.id" class="grid grid-cols-6 hover:bg-slate-200 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <p class="text-sm text-black">{{ item.productName }}</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="text-sm text-black">{{ item.category }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm font-medium" :class="getStockClass(item.currentStock, item.minStock)">
            {{ item.currentStock }}
          </p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black">{{ item.minStock }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black">{{ item.maxStock }}</p>
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
          <h3 class="text-lg font-medium text-black">
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
            <label class="mb-2 block text-sm font-medium text-black">
              محصول
            </label>
            <select
              v-model="adjustmentForm.productId"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
            >
              <option value="">محصول را انتخاب کنید</option>
              <option v-for="item in sampleInventory" :key="item.id" :value="item.id">
                {{ item.productName }} (موجودی فعلی: {{ item.currentStock }})
              </option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black">
              نوع تعدیل
            </label>
            <select
              v-model="adjustmentForm.type"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
            >
              <option value="">نوع تعدیل را انتخاب کنید</option>
              <option value="increase">افزایش موجودی</option>
              <option value="decrease">کاهش موجودی</option>
            </select>
          </div>

          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-black">
              مقدار
            </label>
            <input
              v-model="adjustmentForm.quantity"
              type="number"
              min="1"
              required
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
              placeholder="مقدار تعدیل"
            />
          </div>

          <div class="mb-6">
            <label class="mb-2 block text-sm font-medium text-black">
              دلیل تعدیل
            </label>
            <textarea
              v-model="adjustmentForm.reason"
              rows="3"
              class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
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
              class="flex-1 rounded border border-stroke px-4 py-2 text-black hover:bg-gray-50 dark:border-strokedark dark:hover:bg-meta-4"
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
import { ref, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import { useProductsStore } from '@/stores/products'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import InventoryCard from '@/components/common/InventoryCard.vue'

const inventoryStore = useInventoryStore()
const productsStore = useProductsStore()

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

// Sample inventory data
const sampleInventory = ref([
  {
    id: 1,
    productName: 'دریل برقی 18 ولت',
    category: 'ابزار برقی',
    currentStock: 25,
    minStock: 5,
    maxStock: 50
  },
  {
    id: 2,
    productName: 'چکش ضربه‌ای',
    category: 'ابزار دستی',
    currentStock: 3,
    minStock: 10,
    maxStock: 30
  },
  {
    id: 3,
    productName: 'متر لیزری',
    category: 'ابزار اندازه‌گیری',
    currentStock: 0,
    minStock: 5,
    maxStock: 20
  },
  {
    id: 4,
    productName: 'اره برقی',
    category: 'ابزار برقی',
    currentStock: 15,
    minStock: 3,
    maxStock: 25
  },
  {
    id: 5,
    productName: 'آچار فرانسه',
    category: 'ابزار دستی',
    currentStock: 40,
    minStock: 10,
    maxStock: 60
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

const handleAdjustment = async () => {
  const result = await inventoryStore.createAdjustment(adjustmentForm.value)
  if (result.success) {
    closeAdjustmentModal()
  } else {
    alert('خطا در تعدیل موجودی: ' + result.error)
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    inventoryStore.fetchStockLevels(),
    inventoryStore.fetchWarehouses(),
    productsStore.fetchProducts()
  ])
})
</script>
