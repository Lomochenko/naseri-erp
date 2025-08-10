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
      <div class="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-3 lg:grid-cols-4 xl:gap-6 2xl:gap-7.5 mb-6 max-w-7xl">
        <!-- Total Products Card -->
        <InventoryCard :value="inventoryStore.totalProducts" label="کل محصولات" type="total" />

        <!-- In Stock Products Card -->
        <InventoryCard :value="inventoryStore.inStockProducts" label="محصولات موجود" type="success" />

        <!-- Low Stock Products Card -->
        <InventoryCard :value="inventoryStore.lowStockProducts" label="موجودی کم" type="warning" />

        <!-- Out of Stock Products Card -->
        <InventoryCard :value="inventoryStore.outOfStockProducts" label="ناموجود" type="danger" />
      </div>
      <!-- Action Buttons -->
      <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="flex gap-3">
          <button @click="showAdjustmentModal = true"
            class="inline-flex items-center justify-center rounded-md border-[1.5px] border-gray-200 bg-primary px-6 py-3 text-center font-medium text-dark dark:text-white">
            <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            تعدیل موجودی
          </button>

        </div>

        <!-- Search -->
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="جستجو در موجودی..."
            class="w-full rounded-lg border-[1.5px] border-stroke bg-transparent py-3 pl-12 pr-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary" />
          <svg class="absolute left-2 top-1/2 h-5 w-5 -translate-y-1/2 text-black dark:text-white" fill="none"
            stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <!-- Inventory Table -->
      <div
        class="rounded-sm border border-stroke  bg-slate-100 dark:bg-slate-300  shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5 flex items-center justify-between">
        <h4 class="text-xl font-semibold text-black">
          وضعیت موجودی محصولات
        </h4>
        <button
          @click="showAllAdjustmentHistory = true"
          class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          تاریخچه کامل تعدیلات
        </button>
      </div>

        <div
          class="grid grid-cols-6 bg-slate-100 dark:bg-slate-300 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
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

        <!-- Inventory Data -->
        <div v-for="product in filteredInventoryProducts" :key="product.id"
          class="grid grid-cols-6 hover:bg-slate-200 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
          <div class="col-span-2 flex items-center">
            <div class="flex flex-col gap-1">
              <p class="text-sm font-medium text-black">{{ product.name }}</p>
              <p class="text-xs text-gray-500">کد: {{ product.code }}</p>
            </div>
          </div>
          <div class="col-span-1 hidden items-center sm:flex">
            <p class="text-sm text-black">{{ product.category_name || '-' }}</p>
          </div>
          <div class="col-span-1 flex items-center">
            <p class="text-sm font-medium" :class="getStockClass(product.current_stock, product.min_stock)">
              {{ product.current_stock || 0 }}
            </p>
          </div>
          <div class="col-span-1 flex items-center">
            <p class="text-sm text-black">{{ product.min_stock || 0 }}</p>
          </div>
          <div class="col-span-1 flex items-center">
            <p class="text-sm text-black">{{ product.max_stock || '-' }}</p>
          </div>
          <div class="col-span-1 flex items-center">
            <span :class="getStatusClass(product.current_stock, product.min_stock)"
              class="inline-flex rounded-full bg-opacity-10 px-3 py-1 text-sm font-medium">
              {{ getStatusText(product.current_stock, product.min_stock) }}
            </span>
          </div>
          <div class="col-span-1 flex items-center space-x-2">
            <button @click="adjustStock(product)" class="hover:text-primary" title="تعدیل موجودی">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button @click="deleteProduct(product.id)" class="hover:text-danger ml-2" title="حذف">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Loading more indicator -->
        <div v-if="isLoadingMore" class="px-4 py-6 text-center">
          <LoadingSpinner text="در حال بارگذاری محصولات بیشتر..." />
        </div>

        <!-- Load more button -->
        <div v-if="productsStore.hasNextPage && !isLoadingMore" class="px-4 py-6 text-center">
          <button @click="loadMoreProducts"
            class="rounded-lg bg-primary px-6 py-3 text-white hover:bg-opacity-90 transition-colors">
            نمایش محصولات بیشتر
          </button>
        </div>
        <!-- Total count info -->
        <div v-if="productsStore.totalProducts > 0" class="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
          نمایش {{ productsStore.products.length }} از {{ productsStore.totalProducts }} محصول
        </div>
      </div>

      <!-- Stock Adjustment Modal -->
      <div v-if="showAdjustmentModal"
        class="fixed inset-0 z-50 flex items-center justify-center lg:justify-start bg-slate-800 bg-opacity-50 p-4">
        <div
          class="w-full max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl rounded-lg bg-white p-6 dark:bg-boxdark max-h-[70vh] overflow-y-auto">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-medium text-black">
              تعدیل موجودی
            </h3>
            <button @click="closeAdjustmentModal" class="text-red-600 hover:text-red-800">
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
              <!-- Search Input with Dropdown -->
              <div class="relative mb-2">
                <input ref="productSearchRef" v-model="productSearchQuery" @focus="showSearchDropdown = true"
                  @blur="hideSearchDropdown" type="text" placeholder="جستجو محصولات..."
                  class="w-full rounded border border-stroke bg-transparent px-3 py-2 pr-8 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary transition-all" />
                <svg class="absolute right-2 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" fill="none"
                  stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>

                <!-- Search Results Dropdown -->
                <div v-if="showSearchDropdown && productSearchQuery && filteredProductsForAdjustment.length > 0"
                  class="absolute top-full left-0 right-0 z-10 bg-white dark:bg-boxdark border border-stroke dark:border-strokedark rounded-md shadow-lg max-h-48 overflow-y-auto transition-all duration-200 ease-in-out transform opacity-100 translate-y-0">
                  <div v-for="product in filteredProductsForAdjustment.slice(0, 8)" :key="product.id"
                    @mousedown="selectProductFromDropdown(product)"
                    class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-meta-4 cursor-pointer border-b border-gray-100 dark:border-strokedark last:border-b-0 transition-colors">
                    <div class="flex justify-between items-center">
                      <span class="text-sm font-medium text-black dark:text-white">{{ product.name }}</span>
                      <span class="text-xs text-gray-500 dark:text-gray-400">موجودی: {{ product.current_stock || 0
                        }}</span>
                    </div>
                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">کد: {{ product.code }}</p>
                  </div>
                </div>
              </div>
              <!-- Product Selection -->
              <select v-model="adjustmentForm.productId" required
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary">
                <option value="">محصول را انتخاب کنید</option>
                <option v-for="product in productsStore.products" :key="product.id" :value="product.id">
                  {{ product.name }} (موجودی فعلی: {{ product.current_stock || 0 }})
                </option>
              </select>
            </div>

            <div class="mb-4">
              <label class="mb-2 block text-sm font-medium text-black">
                نوع تعدیل
              </label>
              <select v-model="adjustmentForm.type" required
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary">
                <option value="">نوع تعدیل را انتخاب کنید</option>
                <option value="increase">افزایش موجودی</option>
                <option value="decrease">کاهش موجودی</option>
              </select>
            </div>

            <div class="mb-4">
              <label class="mb-2 block text-sm font-medium text-black">
                مقدار
              </label>
              <input v-model="adjustmentForm.quantity" type="number" min="1" required
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
                placeholder="مقدار تعدیل" />
            </div>

            <div class="mb-6">
              <label class="mb-2 block text-sm font-medium text-black">
                دلیل تعدیل
              </label>
              <textarea v-model="adjustmentForm.reason" rows="3"
                class="w-full rounded border border-stroke bg-transparent px-3 py-2 text-black outline-none focus:border-primary dark:border-strokedark dark:bg-meta-4 dark:focus:border-primary"
                placeholder="دلیل تعدیل موجودی"></textarea>
            </div>

            <div class="flex gap-3">
              <button type="submit" class="flex-1 rounded bg-primary px-4 py-2 text-white hover:bg-opacity-90">
                تعدیل موجودی
              </button>
              <button type="button" @click="closeAdjustmentModal"
                class="flex-1 rounded border border-stroke px-4 py-2 text-black hover:bg-gray-50 dark:border-strokedark dark:hover:bg-meta-4">
                انصراف
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Adjustment History Modal -->
      <AdjustmentHistory v-if="showHistoryModal" :product="selectedProductForHistory" @close="closeHistoryModal" />
      
      <!-- All Adjustment History Modal -->
      <AllAdjustmentHistory v-if="showAllAdjustmentHistory" @close="showAllAdjustmentHistory = false" />
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import { useProductsStore } from '@/stores/products'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import InventoryCard from '@/components/common/InventoryCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AdjustmentHistory from '@/components/inventory/AdjustmentHistory.vue'
import AllAdjustmentHistory from '@/components/inventory/AllAdjustmentHistory.vue'

const inventoryStore = useInventoryStore()
const productsStore = useProductsStore()

// Reactive data
const searchQuery = ref('')
const productSearchQuery = ref('')
const showAdjustmentModal = ref(false)
const showHistoryModal = ref(false)
const showAllAdjustmentHistory = ref(false)
const selectedProductForHistory = ref(null)
const isLoadingMore = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const showSearchDropdown = ref(false)
const productSearchRef = ref(null)

const adjustmentForm = ref({
  productId: '',
  type: '',
  quantity: '',
  reason: ''
})

// Computed properties
const filteredInventoryProducts = computed(() => {
  if (!productsStore.products) return []

  let products = productsStore.products

  if (searchQuery.value) {
    products = products.filter(product =>
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.code.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (product.category_name && product.category_name.toLowerCase().includes(searchQuery.value.toLowerCase()))
    )
  }

  return products
})

const filteredProductsForAdjustment = computed(() => {
  if (!productsStore.products) return []

  let products = productsStore.products

  if (productSearchQuery.value) {
    products = products.filter(product =>
      product.name.toLowerCase().includes(productSearchQuery.value.toLowerCase()) ||
      product.code.toLowerCase().includes(productSearchQuery.value.toLowerCase()) ||
      (product.category_name && product.category_name.toLowerCase().includes(productSearchQuery.value.toLowerCase()))
    )
  }

  return products
})

const deleteProduct = async (id) => {
  if (confirm('آیا از حذف این محصول اطمینان دارید؟')) {
    const result = await productsStore.deleteProduct(id)
    if (!result.success) {
      alert('خطا در حذف محصول: ' + result.error)
    }
  }
}

// Methods for infinite scroll
const loadMoreProducts = async () => {
  if (productsStore.hasNextPage && !isLoadingMore.value) {
    isLoadingMore.value = true
    currentPage.value++
    await productsStore.fetchProducts({
      page: currentPage.value,
      page_size: pageSize.value,
      append: true
    })
    isLoadingMore.value = false
  }
}

// Inventory data comes from products store now via API

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
  selectedProductForHistory.value = item
  showHistoryModal.value = true
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
  selectedProductForHistory.value = null
}

const closeAdjustmentModal = () => {
  showAdjustmentModal.value = false
  productSearchQuery.value = ''
  showSearchDropdown.value = false
  adjustmentForm.value = {
    productId: '',
    type: '',
    quantity: '',
    reason: ''
  }
}

// Search dropdown methods
const selectProductFromDropdown = (product) => {
  adjustmentForm.value.productId = product.id
  productSearchQuery.value = product.name
  showSearchDropdown.value = false
}

const hideSearchDropdown = () => {
  // Use setTimeout to allow click events to fire first
  setTimeout(() => {
    showSearchDropdown.value = false
  }, 150)
}

const handleAdjustment = async () => {
  const result = await inventoryStore.createAdjustment(adjustmentForm.value)
  if (result.success) {
    // Refresh products data to show updated stock counts
    await productsStore.fetchProducts({ page: 1, page_size: pageSize.value })
    // Reset pagination to first page to ensure fresh data
    currentPage.value = 1
    closeAdjustmentModal()
  } else {
    alert('خطا در تعدیل موجودی: ' + result.error)
  }
}

// Infinite scroll functionality
const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight

  // Load more when user scrolls to bottom 200px
  if (scrollTop + windowHeight >= documentHeight - 200 && !isLoadingMore.value && productsStore.hasNextPage) {
    loadMoreProducts()
  }
}

// Lifecycle
onMounted(async () => {
  // Add scroll event listener for infinite scroll
  window.addEventListener('scroll', handleScroll)

  await Promise.all([
    inventoryStore.fetchStockLevels(),
    inventoryStore.fetchWarehouses(),
    productsStore.fetchProducts({ page: currentPage.value, page_size: pageSize.value })
  ])
})

// Cleanup on unmount
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
