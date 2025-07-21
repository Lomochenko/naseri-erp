<template>
  <div class="hidden lg:block search-container">
    <form @submit.prevent="handleSearch">
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در محصولات و مشتریان..."
          class="h-11 w-full rounded-lg border border-gray-200 bg-transparent py-2.5 pl-12 pr-14 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden focus:ring-3 focus:ring-brand-500/10 dark:border-gray-800 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/50 dark:focus:border-brand-800 xl:w-[430px]"
          @input="handleInput"
          @focus="showResults = true"
        />

        <!-- Search Icon -->
        <div class="absolute right-3 top-1/2 -translate-y-1/2">
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        <button
          type="submit"
          class="absolute left-2.5 top-1/2 inline-flex -translate-y-1/2 items-center gap-0.5 rounded-lg border border-gray-200 bg-gray-50 px-[9px] py-[4.5px] text-xs -tracking-[0.2px] text-gray-500 dark:border-gray-800 dark:bg-white/[0.03] dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/[0.05] transition-colors"
        >
          <span>جستجو</span>
          <span class="mt-[5px]">⌘</span>
        </button>

        <!-- Search Results Dropdown -->
        <div
          v-if="showResults && (searchResults.products.length > 0 || searchResults.customers.length > 0 || searchQuery.length > 0)"
          class="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto"
        >
          <!-- Loading State -->
          <div v-if="isLoading" class="p-4 text-center text-gray-500 dark:text-gray-400">
            <div class="animate-spin w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full mx-auto mb-2"></div>
            در حال جستجو...
          </div>

          <!-- No Results -->
          <div v-else-if="searchQuery.length > 0 && searchResults.products.length === 0 && searchResults.customers.length === 0"
               class="p-4 text-center text-gray-500 dark:text-gray-400">
            نتیجه‌ای یافت نشد
          </div>

          <!-- Products Results -->
          <div v-if="searchResults.products.length > 0">
            <div class="px-4 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800">
              محصولات
            </div>
            <div class="max-h-48 overflow-y-auto">
              <button
                v-for="product in searchResults.products.slice(0, 5)"
                :key="`product-${product.id}`"
                @click="selectResult('product', product)"
                class="w-full px-4 py-3 text-right hover:bg-gray-50 dark:hover:bg-gray-800 border-b border-gray-100 dark:border-gray-700 last:border-b-0"
              >
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-brand-100 dark:bg-brand-900/20 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-brand-600 dark:text-brand-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {{ product.name }}
                    </div>
                    <div class="text-xs text-gray-500 dark:text-gray-400 truncate">
                      کد: {{ product.code }} | {{ formatPrice(product.selling_price) }}
                    </div>
                  </div>
                </div>
              </button>
            </div>
          </div>

          <!-- Customers Results -->
          <div v-if="searchResults.customers.length > 0">
            <div class="px-4 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800">
              مشتریان
            </div>
            <div class="max-h-48 overflow-y-auto">
              <button
                v-for="customer in searchResults.customers.slice(0, 5)"
                :key="`customer-${customer.id}`"
                @click="selectResult('customer', customer)"
                class="w-full px-4 py-3 text-right hover:bg-gray-50 dark:hover:bg-gray-800 border-b border-gray-100 dark:border-gray-700 last:border-b-0"
              >
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {{ customer.name }}
                    </div>
                    <div class="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {{ customer.phone_number || customer.phone }}
                    </div>
                  </div>
                </div>
              </button>
            </div>
          </div>

          <!-- View All Results -->
          <div v-if="searchQuery.length > 0 && (searchResults.products.length > 5 || searchResults.customers.length > 5)"
               class="border-t border-gray-200 dark:border-gray-700">
            <button
              @click="viewAllResults"
              class="w-full px-4 py-3 text-sm text-brand-600 dark:text-brand-400 hover:bg-gray-50 dark:hover:bg-gray-800 font-medium"
            >
              مشاهده همه نتایج ({{ totalResults }})
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>

  <!-- Mobile Search -->
  <div class="lg:hidden w-full" v-if="showMobileSearch">
    <form @submit.prevent="handleSearch" class="relative">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="جستجو..."
        class="w-full h-10 rounded-lg border border-gray-200 bg-transparent py-2 pl-10 pr-4 text-sm text-gray-800 placeholder:text-gray-400 focus:border-brand-300 focus:outline-hidden dark:border-gray-800 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-white/50"
        @input="handleInput"
      />
      <div class="absolute right-3 top-1/2 -translate-y-1/2">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useSalesStore } from '@/stores/sales'

const router = useRouter()
const productsStore = useProductsStore()
const salesStore = useSalesStore()

// Props
const props = defineProps({
  showMobileSearch: {
    type: Boolean,
    default: false
  }
})

// Reactive data
const searchQuery = ref('')
const showResults = ref(false)
const isLoading = ref(false)
const searchResults = ref({
  products: [],
  customers: []
})

// Computed
const totalResults = computed(() => {
  return searchResults.value.products.length + searchResults.value.customers.length
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const handleInput = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = { products: [], customers: [] }
    return
  }

  isLoading.value = true

  try {
    // Search products
    const productResults = productsStore.products.filter(product =>
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.code.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (product.description && product.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
    )

    // Search customers
    const customerResults = salesStore.customers.filter(customer =>
      customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (customer.phone_number && customer.phone_number.includes(searchQuery.value)) ||
      (customer.phone && customer.phone.includes(searchQuery.value))
    )

    searchResults.value = {
      products: productResults,
      customers: customerResults
    }
  } catch (error) {
    console.error('Search error:', error)
  } finally {
    isLoading.value = false
  }
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // Navigate to search results page or perform global search
    router.push({
      path: '/search',
      query: { q: searchQuery.value.trim() }
    })
    showResults.value = false
  }
}

const selectResult = (type, item) => {
  showResults.value = false
  searchQuery.value = ''

  if (type === 'product') {
    router.push(`/products`)
  } else if (type === 'customer') {
    router.push(`/customers`)
  }
}

const viewAllResults = () => {
  handleSearch()
}

const closeResults = () => {
  showResults.value = false
}

// Click outside to close
const handleClickOutside = (event) => {
  if (!event.target.closest('.search-container')) {
    showResults.value = false
  }
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  // Cmd/Ctrl + K to focus search
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    const searchInput = document.querySelector('input[placeholder*="جستجو"]')
    if (searchInput) {
      searchInput.focus()
    }
  }

  // Escape to close results
  if (event.key === 'Escape') {
    showResults.value = false
  }
}

// Watchers
watch(searchQuery, (newValue) => {
  if (newValue.length === 0) {
    searchResults.value = { products: [], customers: [] }
    showResults.value = false
  }
})

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)

  // Load initial data if not already loaded
  if (productsStore.products.length === 0) {
    productsStore.fetchProducts()
  }
  if (salesStore.customers.length === 0) {
    salesStore.fetchCustomers()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.search-container {
  position: relative;
}
</style>
