<template>
  <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
    <!-- Header -->
    <div class="px-4 py-6 md:px-6 xl:px-7.5 flex items-center justify-between">
      <h4 class="text-xl font-semibold text-black dark:text-white">
        سفارشات فروش
      </h4>
      <div class="flex gap-2">
        <button @click="showCreateModal = true"
          class="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90 transition-colors">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          سفارش جدید
        </button>
        <button @click="refreshData"
          class="inline-flex items-center gap-2 rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          بروزرسانی
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="border-b border-stroke px-4 py-4 dark:border-strokedark">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:gap-6">
        <!-- Search -->
        <div class="flex-1">
          <input v-model="searchQuery" type="text" placeholder="جستجو در سفارشات..."
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
        </div>

        <!-- Status Filter -->
        <select v-model="statusFilter"
          class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="">همه وضعیت‌ها</option>
          <option value="draft">پیش‌نویس</option>
          <option value="confirmed">تأیید شده</option>
          <option value="completed">تکمیل شده</option>
          <option value="cancelled">لغو شده</option>
        </select>

        <!-- Customer Filter -->
        <select v-model="customerFilter"
          class="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
          <option value="">همه مشتریان</option>
          <option v-for="customer in customers" :key="customer.id" :value="customer.id">
            {{ customer.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <LoadingSpinner text="در حال بارگذاری سفارشات..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredOrders.length === 0 && !loading" class="flex flex-col items-center justify-center p-12">
      <svg class="h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">هیچ سفارشی یافت نشد</h3>
      <p class="text-gray-500 mb-4">برای شروع، اولین سفارش فروش خود را ایجاد کنید</p>
      <button @click="showCreateModal = true"
        class="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-opacity-90 transition-colors">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        ایجاد سفارش جدید
      </button>
    </div>

    <!-- Sales Orders Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full table-auto">
        <thead>
          <tr class="bg-gray-2 text-right dark:bg-meta-4">
            <th class="px-4 py-4 font-medium text-black dark:text-white xl:pl-11">شماره فاکتور</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">مشتری</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">تاریخ</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">وضعیت</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">مبلغ کل</th>
            <th class="px-4 py-4 font-medium text-black dark:text-white">عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in paginatedOrders" :key="order.id"
            class="border-b border-stroke dark:border-strokedark hover:bg-gray-50 dark:hover:bg-gray-800">
            <td class="px-4 py-5 pl-9 xl:pl-11">
              <h5 class="font-medium text-black dark:text-white">{{ order.invoice_number || 'در انتظار تولید' }}</h5>
            </td>
            <td class="px-4 py-5">
              <p class="text-black dark:text-white">{{ order.customer_name }}</p>
            </td>
            <td class="px-4 py-5">
              <p class="text-black dark:text-white">{{ formatDate(order.sale_date) }}</p>
            </td>
            <td class="px-4 py-5">
              <span :class="getStatusClass(order.status)"
                class="inline-flex rounded-full px-3 py-1 text-xs font-medium">
                {{ getStatusText(order.status) }}
              </span>
            </td>
            <td class="px-4 py-5">
              <p class="text-black dark:text-white font-medium">{{ formatPrice(order.total) }}</p>
            </td>
            <td class="px-4 py-5">
              <div class="flex items-center space-x-3.5 space-x-reverse">
                <!-- View -->
                <button @click="viewOrder(order)" class="hover:text-primary" title="مشاهده">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>

                <!-- Edit -->
                <button v-if="order.status === 'draft'" @click="editOrder(order)" class="hover:text-primary" title="ویرایش">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>

                <!-- Status Actions -->
                <div class="relative">
                  <button @click="toggleStatusMenu(order.id)" class="hover:text-primary" title="تغییر وضعیت">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                    </svg>
                  </button>

                  <!-- Status Menu -->
                  <div v-if="activeStatusMenu === order.id"
                    class="absolute right-0 top-8 z-10 w-48 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 dark:bg-gray-800">
                    <div class="py-1">
                      <button v-if="order.status === 'draft'" @click="updateOrderStatus(order, 'confirmed')"
                        class="block w-full px-4 py-2 text-right text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                        تأیید سفارش
                      </button>
                      <button v-if="order.status === 'confirmed'" @click="updateOrderStatus(order, 'completed')"
                        class="block w-full px-4 py-2 text-right text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">
                        تکمیل سفارش
                      </button>
                      <button v-if="['draft', 'confirmed'].includes(order.status)" @click="updateOrderStatus(order, 'cancelled')"
                        class="block w-full px-4 py-2 text-right text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-700">
                        لغو سفارش
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Delete -->
                <button v-if="order.status === 'draft'" @click="deleteOrder(order)" class="hover:text-danger" title="حذف">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-stroke px-4 py-4 dark:border-strokedark">
      <div class="text-sm text-gray-700 dark:text-gray-300">
        نمایش {{ (currentPage - 1) * pageSize + 1 }} تا {{ Math.min(currentPage * pageSize, filteredOrders.length) }} از {{ filteredOrders.length }} سفارش
      </div>
      <div class="flex items-center gap-2">
        <button @click="currentPage--" :disabled="currentPage === 1"
          class="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-50 dark:border-gray-600">
          قبلی
        </button>
        <span class="px-3 py-1 text-sm">{{ currentPage }} از {{ totalPages }}</span>
        <button @click="currentPage++" :disabled="currentPage === totalPages"
          class="rounded-lg border border-gray-300 px-3 py-1 text-sm disabled:opacity-50 dark:border-gray-600">
          بعدی
        </button>
      </div>
    </div>

    <!-- Modals -->
    <SalesOrderForm v-if="showCreateModal" @close="showCreateModal = false" @saved="handleOrderSaved" />
    <SalesOrderForm v-if="showEditModal" :sales-order="editingOrder" @close="showEditModal = false" @saved="handleOrderSaved" />
    <SalesOrderView v-if="showViewModal" :sales-order="viewingOrder" @close="showViewModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import SalesOrderForm from './SalesOrderForm.vue'
import SalesOrderView from './SalesOrderView.vue'

// Store
const salesStore = useSalesStore()

// State
const searchQuery = ref('')
const statusFilter = ref('')
const customerFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showViewModal = ref(false)
const editingOrder = ref(null)
const viewingOrder = ref(null)
const loading = ref(false)
const activeStatusMenu = ref(null)

// Computed
const customers = computed(() => salesStore.customers)
const salesOrders = computed(() => salesStore.salesOrders)

const filteredOrders = computed(() => {
  let filtered = salesOrders.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(order =>
      order.invoice_number.toLowerCase().includes(query) ||
      order.customer_name.toLowerCase().includes(query) ||
      order.notes?.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(order => order.status === statusFilter.value)
  }

  if (customerFilter.value) {
    filtered = filtered.filter(order => order.customer === parseInt(customerFilter.value))
  }

  return filtered
})

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredOrders.value.slice(start, start + pageSize.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredOrders.value.length / pageSize.value)
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR-u-ca-persian')
}

const getStatusText = (status) => {
  const statusMap = {
    'draft': 'پیش‌نویس',
    'confirmed': 'تأیید شده',
    'completed': 'تکمیل شده',
    'cancelled': 'لغو شده'
  }
  return statusMap[status] || status
}

const getStatusClass = (status) => {
  const classMap = {
    'draft': 'bg-gray-100 text-gray-800',
    'confirmed': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'cancelled': 'bg-red-100 text-red-800'
  }
  return classMap[status] || 'bg-gray-100 text-gray-800'
}

const viewOrder = (order) => {
  viewingOrder.value = order
  showViewModal.value = true
}

const editOrder = (order) => {
  editingOrder.value = order
  showEditModal.value = true
}

const deleteOrder = async (order) => {
  if (confirm(`آیا از حذف سفارش ${order.invoice_number} اطمینان دارید؟`)) {
    const result = await salesStore.deleteSalesOrder(order.id)
    if (!result.success) {
      alert('خطا در حذف سفارش: ' + result.error)
    }
  }
}

const toggleStatusMenu = (orderId) => {
  activeStatusMenu.value = activeStatusMenu.value === orderId ? null : orderId
}

const updateOrderStatus = async (order, newStatus) => {
  const result = await salesStore.updateSalesOrder(order.id, { status: newStatus })
  if (result.success) {
    activeStatusMenu.value = null
  } else {
    alert('خطا در تغییر وضعیت: ' + result.error)
  }
}

const refreshData = async () => {
  await salesStore.fetchSalesOrders()
}

const handleOrderSaved = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingOrder.value = null
  refreshData()
}

// Close status menu when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeStatusMenu.value = null
  }
}

// Lifecycle
onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  loading.value = true
  try {
    await Promise.all([
      salesStore.fetchSalesOrders(),
      salesStore.fetchCustomers()
    ])
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
