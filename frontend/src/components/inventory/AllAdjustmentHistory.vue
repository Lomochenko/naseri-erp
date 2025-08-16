<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center lg:justify-start bg-black bg-opacity-50 p-0 lg:p-4"
    @click.self="handleOverlayClick">
    <!-- Modal container - full screen on mobile, centered on desktop -->
    <div
      class="w-full h-full lg:w-auto lg:max-w-4xl lg:h-[70vh] rounded-lg bg-white shadow-xl flex flex-col overflow-visible relative">

      <!-- Close button for large screens (top-left corner with blinking effect) -->
      <button @click="$emit('close')"
        class="hidden lg:block absolute -top-2 -left-2 z-50 rounded-full p-2 bg-red-500 text-white shadow-lg animate-pulse">
        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Filters Container (sticky with collapse animation) -->
      <div ref="filtersContainer" :class="[
        'sticky z-20 bg-white border-b border-gray-200 overflow-hidden transition-all duration-300 ease-in-out',
        showFilters ? 'max-h-60' : 'max-h-0 border-b-0',
        'pt-16 lg:pt-0'  // Add top padding for mobile header space
      ]">
        <div class="px-6 py-4">
          <!-- Mobile layout (column) -->
          <div class="flex flex-col gap-4 md:flex-row md:gap-6 md:items-center">
            <!-- Mobile: Top row (search + close button) -->
            <div class="flex gap-2 items-center w-full">

              <!-- Search -->
              <div class="flex-1">
                <input v-model="searchQuery" type="text" placeholder="جستجو در محصولات..."
                class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none" />
              </div>
              <!-- Close button for mobile -->
              <button @click="$emit('close')"
                class="lg:hidden rounded-lg p-2 bg-red-500 text-white shadow animate-pulse">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Filters row (adjustment type + date pickers) -->
            <div class="flex flex-col sm:flex-row gap-4 w-full">
              <!-- Adjustment Type Filter -->
              <select v-model="adjustmentTypeFilter"
                class="w-full sm:w-auto rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none">
                <option value="">همه تعدیلات</option>
                <option value="increase">افزایش موجودی</option>
                <option value="decrease">کاهش موجودی</option>
              </select>

              <!-- Date Range -->
              <div class="flex flex-row gap-2 w-full">
                <DatePicker v-model="dateFrom" format="YYYY/MM/DD" display-format="jYYYY/jMM/jDD" :editable="false"
                  :clearable="true" placeholder="از تاریخ"
                  class="flex-1 min-w-[120px] rounded-lg border-0 outline outline-gray-300 px-2 py-1 text-sm focus:outline-primary focus:outline-none"
                  @open="isCalendarOpen = true" @close="isCalendarOpen = false" />
                <DatePicker v-model="dateTo" format="YYYY/MM/DD" display-format="jYYYY/jMM/jDD" :editable="false"
                  :clearable="true" placeholder="تا تاریخ"
                  class="flex-1 min-w-[120px] rounded-lg border-0 outline outline-gray-300 px-2 py-1 text-sm focus:outline-primary focus:outline-none "
                  @open="isCalendarOpen = true" @close="isCalendarOpen = false" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto" ref="scrollContainer">
        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center p-8">
          <LoadingSpinner text="در حال بارگذاری تاریخچه..." />
        </div>

        <!-- History List -->
        <div v-else>
          <div v-if="filteredAdjustments.length === 0" class="flex items-center justify-center p-8">
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2V9a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <p class="mt-4 text-gray-500">هیچ تعدیلی یافت نشد</p>
            </div>
          </div>

          <!-- Adjustment Cards -->
          <div v-else class="space-y-4 p-6">
            <div v-for="adjustment in paginatedAdjustments" :key="adjustment.id"
              class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800">
              <!-- Adjustment Header -->
              <div class="flex items-center justify-between border-b border-gray-100 pb-3 dark:border-gray-700">
                <div class="flex items-center gap-3">
                  <!-- Type Icon -->
                  <div
                    :class="adjustment.adjustment_type === 'add' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'"
                    class="flex h-10 w-10 items-center justify-center rounded-full">
                    <svg v-if="adjustment.adjustment_type === 'add'" class="h-5 w-5" fill="none" stroke="currentColor"
                      viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
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
                    {{ adjustment.created_by_name || 'نامشخص' }}
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
                        <tr v-for="item in adjustment.items" :key="item.id"
                          class="border-t border-gray-100 dark:border-gray-600">
                          <td class="px-3 py-2 text-gray-900 dark:text-white">{{ item.product_name }}</td>
                          <td class="px-3 py-2">
                            <span :class="adjustment.adjustment_type === 'add' ? 'text-green-600' : 'text-red-600'"
                              class="font-medium">
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
          <div v-if="hasMoreData && !loading" class="border-t border-gray-200 p-4 text-center dark:border-gray-700">
            <button @click="loadMoreAdjustments"
              class="rounded-lg bg-primary px-4 py-2 text-white hover:bg-opacity-90 transition-colors">
              بارگذاری بیشتر
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { inventoryAPI } from '@/services/api'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import DatePicker from 'vue3-persian-datetime-picker'

// Emits
const emit = defineEmits(['close'])

// State
const searchQuery = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const adjustmentTypeFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const scrollContainer = ref(null)
const filtersContainer = ref(null)
const isCalendarOpen = ref(false)

const adjustments = ref([])
const hasMoreData = ref(false)
const loading = ref(false)
const showFilters = ref(true)
const lastScrollPosition = ref(0)

// Computed
const filteredAdjustments = computed(() => {
  let filtered = adjustments.value

  // Search filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter(adj =>
    (adj.items?.some(item => item.product_name?.toLowerCase().includes(q)) ||
      (adj.reason || '').toLowerCase().includes(q))
    )
  }

  // Date filter - now using Gregorian dates
  if (dateFrom.value) {
    const from = new Date(dateFrom.value)
    filtered = filtered.filter(adj => {
      const adjDate = new Date(adj.created_at)
      return adjDate >= from
    })
  }

  if (dateTo.value) {
    const to = new Date(dateTo.value)
    to.setHours(23, 59, 59, 999) // Include entire day
    filtered = filtered.filter(adj => {
      const adjDate = new Date(adj.created_at)
      return adjDate <= to
    })
  }

  // Type filter
  if (adjustmentTypeFilter.value) {
    const type = adjustmentTypeFilter.value === 'increase' ? 'add' : 'subtract'
    filtered = filtered.filter(adj => adj.adjustment_type === type)
  }

  return filtered
})

const paginatedAdjustments = computed(() => {
  return filteredAdjustments.value.slice(0, currentPage.value * pageSize.value)
})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'تاریخ نامشخص'

  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'تاریخ نامعتبر'

    // Format to Persian/Jalali date
    return new Intl.DateTimeFormat('fa-IR-u-ca-persian', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'Asia/Tehran'
    }).format(date)
  } catch (error) {
    console.error('Date formatting error:', error, dateString)
    return 'تاریخ نامعتبر'
  }
}

const fetchAdjustments = async (page = 1, append = false) => {
  try {
    loading.value = true
    const response = await inventoryAPI.getAdjustments({
      page,
      page_size: pageSize.value,
      ordering: '-created_at'
    })

    const results = response.data.results || response.data

    if (append) {
      adjustments.value = [...adjustments.value, ...results]
    } else {
      adjustments.value = results
    }

    hasMoreData.value = Boolean(response.data.next)
  } catch (error) {
    console.error('Error fetching adjustments:', error)
    if (!append) adjustments.value = []
    hasMoreData.value = false
  } finally {
    loading.value = false
  }
}

const loadMoreAdjustments = async () => {
  if (!hasMoreData.value || loading.value) return

  // Save scroll position before loading
  const container = scrollContainer.value
  const scrollTop = container.scrollTop
  const scrollHeight = container.scrollHeight

  currentPage.value += 1
  await fetchAdjustments(currentPage.value, true)

  // Restore scroll position after data loads
  nextTick(() => {
    container.scrollTop = scrollTop + (container.scrollHeight - scrollHeight)
  })
}

// Scroll handling for hiding/showing filters
const handleScroll = () => {
  if (!scrollContainer.value) return

  const currentScrollPosition = scrollContainer.value.scrollTop
  const scrollDirection = currentScrollPosition > lastScrollPosition.value ? 'down' : 'up'

  // Only hide filters if we've scrolled more than 50px
  if (scrollDirection === 'down' && currentScrollPosition > 50) {
    showFilters.value = false
  } else if (scrollDirection === 'up') {
    showFilters.value = true
  }

  // Always show filters when at top of container
  if (currentScrollPosition <= 10) {
    showFilters.value = true
  }

  lastScrollPosition.value = currentScrollPosition
}

// Infinite scroll
const handleInfiniteScroll = () => {
  const el = scrollContainer.value
  if (!el || loading.value || !hasMoreData.value) return
  const threshold = 150
  if (el.scrollTop + el.clientHeight >= el.scrollHeight - threshold) {
    loadMoreAdjustments()
  }
}

// Combined scroll handler
const scrollHandler = () => {
  handleScroll()
  handleInfiniteScroll()
}

// Lifecycle
onMounted(async () => {
  currentPage.value = 1
  await fetchAdjustments(1, false)
  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('scroll', scrollHandler)
  }
})

onUnmounted(() => {
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('scroll', scrollHandler)
  }
})

const handleOverlayClick = () => {
  if (isCalendarOpen.value) return
  emit('close')
}
</script>
