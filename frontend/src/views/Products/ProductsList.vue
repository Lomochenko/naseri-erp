<template>
  <AdminLayout>
    <div>
    <!-- Breadcrumb -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-title-md2 font-bold text-black dark:text-white">
        مدیریت محصولات
      </h2>
      <nav>
        <ol class="flex items-center text-black dark:text-white gap-2">
          <li>
            <router-link class="font-medium" to="/">داشبورد /</router-link>
          </li>
          <li class="font-medium text-primary">محصولات</li>
        </ol>
      </nav>
    </div>

    <!-- Action Buttons -->
    <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex gap-2">
        <router-link
          to="/products/create"
          class="inline-flex items-center justify-center rounded-md border-[1.5px] border-gray-200 bg-primary px-3 py-3 text-center font-medium text-black dark:text-white hover:bg-opacity-90"
        >
        افزودن محصول جدید
        <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        </router-link>
      </div>

      <!-- Search -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در محصولات..."
          class="w-full rounded-lg border-[1.5px] bg-transparent py-3 pr-12 pl-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
        />
        <svg
          class="absolute right-4 top-1/2 h-5 w-5 -translate-y-1/2 text-black dark:text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <!-- Loading -->
    <LoadingSpinner v-if="productsStore.isLoading" text="در حال بارگذاری محصولات..." />

    <!-- Error Message -->
    <ErrorMessage
      v-if="productsStore.error"
      :message="productsStore.error"
      @dismiss="productsStore.clearError"
      class="mb-4"
    />

    <!-- Products Table -->
    <div v-else class="rounded-sm border border-stroke bg-slate-100 dark:bg-slate-300 shadow-default dark:border-strokedark dark:bg-boxdark">
      <div class="px-4 py-6 md:px-6 xl:px-7.5">
        <h4 class="text-xl font-semibold text-black">
          لیست محصولات ({{ productsStore.totalProducts }})
        </h4>
      </div>

      <div class="grid grid-cols-7 border-t border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-9 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <p class="font-medium">نام محصول</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="font-medium">دسته‌بندی</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">قیمت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">موجودی</p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="font-medium">واحد</p>
        </div>
        <div class="col-span-1 hidden items-center lg:flex">
          <p class="font-medium">توضیحات</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">وضعیت</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="font-medium">عملیات</p>
        </div>
      </div>

      <div v-for="product in filteredProducts" :key="product.id" class="grid grid-cols-7 border-t hover:bg-slate-200 border-stroke px-4 py-4.5 dark:border-strokedark sm:grid-cols-9 md:px-6 2xl:px-7.5">
        <div class="col-span-2 flex items-center">
          <div class="flex flex-col gap-1">
            <p class="text-sm font-medium text-black ">{{ product.name }}</p>
            <p class="text-xs text-gray-500">کد: {{ product.code }}</p>
          </div>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="text-sm text-black ">{{ product.category_name || '-' }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm text-black ">{{ formatPrice(product.selling_price) }}</p>
        </div>
        <div class="col-span-1 flex items-center">
          <p class="text-sm" :class="getStockClass(product.current_stock)">
            {{ product.current_stock || 0 }}
          </p>
        </div>
        <div class="col-span-1 hidden items-center sm:flex">
          <p class="text-sm text-black ">{{ product.unit_symbol || '-' }}</p>
        </div>
        <div class="col-span-1 hidden items-center lg:flex">
          <p class="text-sm text-black  truncate max-w-32" :title="product.description">
            {{ product.description ? (product.description.length > 30 ? product.description.substring(0, 30) + '...' : product.description) : '-' }}
          </p>
        </div>
        <div class="col-span-1 flex items-center">
          <span
            :class="product.is_active ? 'bg-success text-success' : 'bg-danger text-danger'"
            class="inline-flex rounded-full bg-opacity-10 px-3 py-1 text-sm font-medium"
          >
            {{ product.is_active ? 'فعال' : 'غیرفعال' }}
          </span>
        </div>
        <div class="col-span-1 flex items-center space-x-2">
          <router-link
            :to="`/products/${product.id}/edit`"
            class="hover:text-primary"
            title="ویرایش"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </router-link>
          <button
            @click="deleteProduct(product.id)"
            class="hover:text-danger ml-2"
            title="حذف"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="productsStore.totalProducts > 0" class="mt-6 flex items-center justify-between">
      <div class="text-sm text-gray-700 dark:text-gray-300">
        نمایش صفحه {{ ((currentPage - 1) * pageSize) + 1 }} <span class="text-lg">↫</span> {{ Math.min(currentPage * pageSize, productsStore.totalProducts) }} محصول از {{ productsStore.totalProducts }}
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="previousPage"
          :disabled="!productsStore.hasPreviousPage"
          class="rounded-lg border border-stroke text-gray-700 dark:text-gray-300 px-3 py-2 text-sm hover:bg-gray-50 disabled:hover:bg-inherit disabled:opacity-50 disabled:cursor-not-allowed dark:border-strokedark dark:hover:bg-meta-4"
        >
          قبلی
        </button>
        <span class="px-3 py-2 text-sm text-gray-700 dark:text-gray-300">صفحه {{ currentPage }}</span>
        <button
          @click="nextPage"
          :disabled="!productsStore.hasNextPage"
          class="rounded-lg border border-stroke text-gray-700 dark:text-gray-300 px-3 py-2 text-sm hover:bg-gray-50 disabled:hover:bg-inherit disabled:opacity-50 disabled:cursor-not-allowed dark:border-strokedark dark:hover:bg-meta-4"
        >
          بعدی
        </button>
      </div>
    </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useProductsStore } from '@/stores/products'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorMessage from '@/components/common/ErrorMessage.vue'

const productsStore = useProductsStore()

// Reactive data
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(20)

// Computed
const filteredProducts = computed(() => {
  if (!searchQuery.value) return productsStore.products

  return productsStore.products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    product.code.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (product.category_name && product.category_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (product.description && product.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
})

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const getStockClass = (stock) => {
  if (stock <= 0) return 'text-danger'
  if (stock <= 10) return 'text-warning'
  return 'text-success'
}

const deleteProduct = async (id) => {
  if (confirm('آیا از حذف این محصول اطمینان دارید؟')) {
    const result = await productsStore.deleteProduct(id)
    if (!result.success) {
      alert('خطا در حذف محصول: ' + result.error)
    }
  }
}

const nextPage = () => {
  if (productsStore.hasNextPage) {
    currentPage.value++
    loadProducts()
  }
}

const previousPage = () => {
  if (productsStore.hasPreviousPage) {
    currentPage.value--
    loadProducts()
  }
}

const loadProducts = async () => {
  await productsStore.fetchProducts({
    page: currentPage.value,
    page_size: pageSize.value
  })
}

// Watchers
watch(searchQuery, () => {
  // Reset to first page when searching
  currentPage.value = 1
})

// Lifecycle
onMounted(async () => {
  // Only fetch categories and units if they haven't been loaded yet
  const promises = [
    productsStore.fetchProducts({ page: currentPage.value, page_size: pageSize.value })
  ]

  if (productsStore.categories.length === 0) {
    promises.push(productsStore.fetchCategories())
  }

  if (productsStore.units.length === 0) {
    promises.push(productsStore.fetchUnits())
  }

  await Promise.all(promises)
})
</script>
