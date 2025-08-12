<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
   <div class="w-full max-w-2xl rounded-lg bg-white shadow-xl dark:bg-boxdark h-[65vh] flex flex-col overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4 dark:border-gray-700">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          تاریخچه کامل تعدیلات موجودی
        </h3>
        <button
          @click="$emit('close')"
          class="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-gray-600 dark:hover:text-gray-300"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Filters -->
      <div class="border-b border-gray-200 px-6 py-4 dark:border-gray-700">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
          <!-- Search -->
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="جستجو در محصولات..."
              class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>

          <!-- Date Range -->
          <div class="flex gap-2">
            <input
              v-model="dateFrom"
              type="date"
              class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
            <span class="flex items-center px-2 text-gray-500">تا</span>
            <input
              v-model="dateTo"
              type="date"
              class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>

          <!-- Adjustment Type Filter -->
          <select
            v-model="adjustmentTypeFilter"
            class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
          >
            <option value="">همه تعدیلات</option>
            <option value="increase">افزایش موجودی</option>
            <option value="decrease">کاهش موجودی</option>
          </select>
        </div>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto">
        <!-- Loading -->
        <div v-if="inventoryStore.isLoading" class="flex items-center justify-center p-8">
          <LoadingSpinner text="در حال بارگذاری تاریخچه..." />
        </div>

        <!-- History List -->
        <div v-else>
          <div v-if="filteredAdjustments.length === 0" class="flex items-center justify-center p-8">
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2V9a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <p class="mt-4 text-gray-500">هیچ تعدیلی یافت نشد</p>
            </div>
          </div>

          <!-- Adjustment Cards -->
          <div v-else class="space-y-4 p-6">
            <div
              v-for="adjustment in paginatedAdjustments"
              :key="adjustment.id"
              class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800"
            >
              <!-- Adjustment Header -->
              <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-700">
                <div class="flex items-center gap-3">
                  <!-- Type Icon -->
                  <div
                    :class="adjustment.adjustment_type === 'add' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'"
                    class="flex h-10 w-10 items-center justify-center rounded-full"
                  >
                    <svg v-if="adjustment.adjustment_type === 'add'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                    </svg>
                  </div>

                  <div>
                    <h4 class="font-medium text-gray-900 dark:text-white">
                      {{ adjustment.adjustment_type === 'add' ? 'افزایش موجودی' : 'کاهش موجودی' }}
                    </h4>
                    <p class="text-sm text-gray-500">
                      {{ formatDate(adjustment.created_at) }}
                    </p>
                  </div>
                </div>

                <!-- User Info -->
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ adjustment.created_by?.first_name }} {{ adjustment.created_by?.last_name }}
                  </p>
                  <p class="text-xs text-gray-500">کاربر</p>
                </div>
              </div>

              <!-- Adjustment Details -->
              <div class="mt-4">
                <div v-if="adjustment.reason" class="mb-3">
                  <p class="text-sm text-gray-600 dark:text-gray-400">
                    <span class="font-medium">دلیل:</span> {{ adjustment.reason }}
                  </p>
                </div>

                <!-- Items -->
                <div class="space-y-2">
                  <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300">آیتم‌های تعدیل شده:</h5>
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm">
                      <thead class="bg-gray-50 dark:bg-gray-700">
                        <tr>
                          <th class="px-3 py-2 text-right font-medium text-gray-700 dark:text-gray-300">محصول</th>
                          <th class="px-3 py-2 text-right font-medium text-gray-700 dark:text-gray-300">مقدار</th>
                          <th class="px-3 py-2 text-right font-medium text-gray-700 dark:text-gray-300">یادداشت</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in adjustment.items"
                          :key="item.id"
                          class="border-t border-gray-100 dark:border-gray-600"
                        >
                          <td class="px-3 py-2 text-gray-900 dark:text-white">{{ item.product_name }}</td>
                          <td class="px-3 py-2">
                            <span
                              :class="adjustment.adjustment_type === 'add' ? 'text-green-600' : 'text-red-600'"
                              class="font-medium"
                            >
                              {{ adjustment.adjustment_type === 'add' ? '+' : '-' }}{{ item.quantity }}
                            </span>
                          </td>
                          <td class="px-3 py-2 text-gray-600 dark:text-gray-400">{{ item.notes || '-' }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Load More Button -->
          <div v-if="hasMoreData && !inventoryStore.isLoading" class="border-t border-gray-200 p-4 text-center dark:border-gray-700">
            <button
              @click="loadMoreAdjustments"
              class="rounded-lg bg-primary px-4 py-2 text-white hover:bg-opacity-90 transition-colors"
            >
              بارگذاری بیشتر
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

// Emits
defineEmits(['close'])

// Store
const inventoryStore = useInventoryStore()

// State
const searchQuery = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const adjustmentTypeFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// Mock data - replace with real API call
const adjustments = ref([])
const hasMoreData = ref(true)

// Computed
const filteredAdjustments = computed(() => {
  let filtered = adjustments.value

  // Search filter
  if (searchQuery.value) {
    filtered = filtered.filter(adj =>
      adj.items.some(item =>
        item.product_name.toLowerCase().includes(searchQuery.value.toLowerCase())
      ) || adj.reason?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Date filter
  if (dateFrom.value) {
    filtered = filtered.filter(adj => new Date(adj.created_at) >= new Date(dateFrom.value))
  }
  if (dateTo.value) {
    filtered = filtered.filter(adj => new Date(adj.created_at) <= new Date(dateTo.value))
  }

  // Type filter
  if (adjustmentTypeFilter.value) {
    const type = adjustmentTypeFilter.value === 'increase' ? 'add' : 'subtract'
    filtered = filtered.filter(adj => adj.adjustment_type === type)
  }

  return filtered
})

const paginatedAdjustments = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredAdjustments.value.slice(0, start + pageSize.value)
})

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadMoreAdjustments = () => {
  currentPage.value++
  // In real implementation, this would load more data from API
}

// Sample data - replace with real API call
const loadAdjustments = async () => {
  // Mock data
  adjustments.value = [
    {
      id: 1,
      adjustment_type: 'add',
      reason: 'موجودی اولیه محصولات جدید',
      created_at: '2025-01-10T08:30:00Z',
      created_by: { first_name: 'علی', last_name: 'احمدی' },
      items: [
        { id: 1, product_name: 'دریل برقی 18 ولت', quantity: 25, notes: 'موجودی اولیه' },
        { id: 2, product_name: 'چکش ضربه‌ای', quantity: 15, notes: 'موجودی اولیه' }
      ]
    },
    {
      id: 2,
      adjustment_type: 'subtract',
      reason: 'کسری موجودی پس از انبارگردانی',
      created_at: '2025-01-09T14:15:00Z',
      created_by: { first_name: 'فاطمه', last_name: 'رضایی' },
      items: [
        { id: 3, product_name: 'متر لیزری', quantity: 3, notes: 'کسری در انبار' }
      ]
    },
    {
      id: 3,
      adjustment_type: 'add',
      reason: 'بازگشت کالا از مشتری',
      created_at: '2025-01-08T10:45:00Z',
      created_by: { first_name: 'محمد', last_name: 'کریمی' },
      items: [
        { id: 4, product_name: 'اره برقی', quantity: 2, notes: 'محصول سالم برگشتی' }
      ]
    }
  ]
}

// Lifecycle
onMounted(async () => {
  await loadAdjustments()
})
</script>
