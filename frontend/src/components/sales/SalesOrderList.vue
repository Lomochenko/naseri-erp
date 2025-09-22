<template>
  <div class="overflow-hidden rounded-xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
    <!-- Header -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
      <div class="flex items-center justify-between">
        <h4 class="text-xl font-semibold text-gray-900 dark:text-white">
          سفارشات فروش
        </h4>
        <div class="flex items-center gap-3">
          <button @click="showCreateModal = true"
            class="inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-black dark:text-white border-2 border-black dark:border-white hover:bg-opacity-90 transition-colors">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            سفارش جدید
          </button>
        </div>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-3 lg:grid-cols-4 xl:gap-6 2xl:gap-7.5 mx-4 my-4">
      <!-- Total Orders Card -->
      <InventoryCard
        :value="salesStats.totalOrders"
        label="کل سفارشات"
        type="total"
      />

      <!-- Today Revenue Card -->
      <InventoryCard
        :value="salesStats.todayRevenue"
        label="درآمد امروز"
        type="success"
      />

      <!-- Pending Orders Card -->
      <InventoryCard
        :value="salesStats.pendingOrders"
        label="سفارشات در انتظار"
        type="warning"
      />

      <!-- Cancelled Orders Card -->
      <InventoryCard
        :value="salesStats.cancelledOrders"
        label="سفارشات لغو شده"
        type="danger"
      />
    </div>

    <!-- Filters -->
    <div class="border-b border-gray-200 bg-gray-50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
      <div class="grid grid-cols-1 gap-4 md:grid-cols-5">
        <!-- Search Input -->
        <div>
          <input v-model="searchQuery" type="text" placeholder="جستجو در سفارشات..."
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white" />
        </div>

        <!-- Status Filter -->
        <div>
          <select v-model="statusFilter"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
            <option value="">همه وضعیت‌ها</option>
            <option value="draft">پیش‌نویس</option>
            <option value="confirmed">تأیید شده</option>
            <option value="completed">تکمیل شده</option>
            <option value="cancelled">لغو شده</option>
          </select>
        </div>

        <!-- Customer Filter -->
        <div>
          <select v-model="customerFilter"
            class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white">
            <option value="">همه مشتریان</option>
            <option v-for="customer in customers" :key="customer.id" :value="customer.id">
              {{ customer.name }}
            </option>
          </select>
        </div>

        <!-- Date From Filter -->
        <div>
          <DatePicker
            v-model="dateFromFilter"
            placeholder="از تاریخ..."
            format="YYYY-MM-DD"
            display-format="jYYYY/jMM/jDD"
            :auto-submit="true"
            :clearable="true"
            class="w-full"
            input-class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-primary focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white"
          />
        </div>

        <!-- Clear Filters Button -->
        <div>
          <button @click="clearFilters"
            class="w-full inline-flex items-center justify-center rounded-md border border-gray-300 px-4 py-2 text-center text-sm text-black hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 transition-colors">
            <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            پاک کردن فیلترها
          </button>
        </div>
      </div>
    </div>

    <!-- Alert Messages -->
    <div v-if="alertMessage.show" class="px-6 py-4">
      <AlertJS
        :variant="alertMessage.type"
        :title="alertMessage.title"
        :message="alertMessage.message"
        @close="alertMessage.show = false"
      />
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
    <div v-else class="max-w-full overflow-x-auto custom-scrollbar">
      <table class="min-w-full">
        <thead>
          <tr class="border-b border-gray-200 dark:border-gray-700">
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">شماره فاکتور</p>
            </th>
            <th class="px-5 py-3 text-right w-3/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">مشتری</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">تاریخ</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">وضعیت</p>
            </th>
            <th class="px-5 py-3 text-right w-2/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">مبلغ کل</p>
            </th>
            <th class="px-5 py-3 text-center w-1/12 sm:px-6">
              <p class="font-medium text-gray-500 text-sm dark:text-gray-400">عملیات</p>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="order in paginatedOrders" :key="order.id"
            class="border-t border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td class="px-5 py-4 sm:px-6">
              <h5 class="font-medium text-black dark:text-white text-sm">
                {{ order.invoice_number || 'در انتظار تولید' }}
              </h5>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p class="text-black dark:text-white text-sm">
                {{ order.customer_name }}
              </p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p class="text-black dark:text-white text-sm">{{ formatDate(order.sale_date) }}</p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <div class="flex items-center gap-2">
                <span :class="[
                  'rounded-full px-2 py-0.5 text-xs font-medium',
                  getStatusClass(order.status)
                ]">
                  {{ getStatusText(order.status) }}
                </span>

                <!-- Status Action Buttons -->
                <div v-if="order.status === 'draft'" class="flex gap-1 mr-2">
                  <button @click="updateOrderStatus(order, 'confirmed')"
                    class="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                    title="تایید سفارش">
                    تایید
                  </button>
                  <button @click="updateOrderStatus(order, 'cancelled')"
                    class="px-2 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                    title="لغو سفارش">
                    لغو
                  </button>
                </div>

                <div v-else-if="order.status === 'confirmed'" class="flex gap-1 mr-2">
                  <button @click="updateOrderStatus(order, 'completed')"
                    class="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                    title="تکمیل سفارش">
                    تکمیل
                  </button>
                  <button @click="updateOrderStatus(order, 'cancelled')"
                    class="px-2 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                    title="لغو سفارش">
                    لغو
                  </button>
                </div>
              </div>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <p class="text-gray-800 text-sm font-medium dark:text-white/90">{{ formatPrice(order.total) }}</p>
            </td>
            <td class="px-5 py-4 sm:px-6">
              <div class="flex items-center justify-center gap-2">
                <!-- View -->
                <button @click="viewOrder(order)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-primary transition-colors"
                  title="مشاهده">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>

                <!-- Edit -->
                <button v-if="order.status === 'draft'" @click="editOrder(order)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-primary transition-colors"
                  title="ویرایش">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>

                <!-- Unified Receipt Button -->
                <button @click="handleReceiptAction(order)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-green-600 transition-colors"
                  title="رسید و QR کد">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </button>

                <!-- Delete -->
                <button v-if="order.status === 'draft'" @click="deleteOrder(order)"
                  class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 hover:text-red-600 transition-colors"
                  title="حذف">
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
    <SalesOrderForm :show="showCreateModal" @close="showCreateModal = false" @saved="handleOrderSaved" />
    <SalesOrderForm :show="showEditModal" :sales-order="editingOrder" @close="showEditModal = false" @saved="handleOrderSaved" />
    <SalesOrderView :show="showViewModal" :sales-order="viewingOrder" @close="showViewModal = false" />
    <ReceiptPrint :show="showReceiptModal" :sales-order="receiptOrder" @close="showReceiptModal = false" />
    <QRScanner :show="showQRScanner" @close="showQRScanner = false" @invoice-found="handleInvoiceFound" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import SalesOrderForm from './SalesOrderForm.vue'
import SalesOrderView from './SalesOrderView.vue'
import ReceiptPrint from './ReceiptPrint.vue'
import QRScanner from './QRScanner.vue'
import AlertJS from '@/components/ui/AlertJS.vue'
import InventoryCard from '@/components/common/InventoryCard.vue'
import DatePicker from 'vue3-persian-datetime-picker'
import { storeInvoiceOffline } from '@/utils/qrCodeUtils'
import { downloadReceiptPDF } from '@/utils/pdfUtils'
import { generateMobileQRCodeURL } from '@/utils/qrCodeUtils'

// Store
const salesStore = useSalesStore()

// State
const searchQuery = ref('')
const statusFilter = ref('')
const customerFilter = ref('')
const dateFromFilter = ref('')
const dateToFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showViewModal = ref(false)
const showReceiptModal = ref(false)
const showQRScanner = ref(false)
const editingOrder = ref(null)
const viewingOrder = ref(null)
const receiptOrder = ref(null)
const loading = ref(false)

// Statistics
const salesStats = ref({
  totalOrders: 0,
  todayRevenue: 0,
  pendingOrders: 0,
  cancelledOrders: 0
})

// Alert system
const alertMessage = ref({
  show: false,
  type: 'info',
  title: '',
  message: ''
})

const showAlert = (type, title, message) => {
  alertMessage.value = {
    show: true,
    type,
    title,
    message
  }
  // Auto hide after 5 seconds
  setTimeout(() => {
    alertMessage.value.show = false
  }, 5000)
}
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

  // Date filtering
  if (dateFromFilter.value) {
    filtered = filtered.filter(order => {
      const orderDate = new Date(order.sale_date)
      const fromDate = new Date(dateFromFilter.value)
      return orderDate >= fromDate
    })
  }

  if (dateToFilter.value) {
    filtered = filtered.filter(order => {
      const orderDate = new Date(order.sale_date)
      const toDate = new Date(dateToFilter.value)
      return orderDate <= toDate
    })
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
    'draft': 'bg-gray-50 text-gray-700 dark:bg-gray-500/15 dark:text-gray-500',
    'confirmed': 'bg-blue-50 text-blue-700 dark:bg-blue-500/15 dark:text-blue-500',
    'completed': 'bg-success-50 text-success-700 dark:bg-success-500/15 dark:text-success-500',
    'cancelled': 'bg-error-50 text-error-700 dark:bg-error-500/15 dark:text-error-500'
  }
  return classMap[status] || 'bg-gray-50 text-gray-700 dark:bg-gray-500/15 dark:text-gray-500'
}

const viewOrder = (order) => {
  viewingOrder.value = order
  showViewModal.value = true
}

const editOrder = (order) => {
  editingOrder.value = order
  showEditModal.value = true
}

const handleReceiptAction = (order) => {
  // Store invoice offline first
  storeInvoiceOffline(order)

  // Show receipt modal with QR code
  receiptOrder.value = order
  showReceiptModal.value = true

  showAlert('success', 'رسید آماده', 'رسید با کد QR آماده مشاهده و چاپ است')
}

const handleInvoiceFound = (invoice) => {
  // Show the found invoice in view modal
  viewingOrder.value = invoice
  showViewModal.value = true
  showAlert('success', 'فاکتور یافت شد', `فاکتور ${invoice.invoice_number || 'بدون شماره'} با موفقیت بازیابی شد`)
}

const deleteOrder = async (order) => {
  if (confirm(`آیا از حذف سفارش ${order.invoice_number} اطمینان دارید؟`)) {
    const result = await salesStore.deleteSalesOrder(order.id)
    if (!result.success) {
      alert('خطا در حذف سفارش: ' + result.error)
    }
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  customerFilter.value = ''
  dateFromFilter.value = ''
  dateToFilter.value = ''
  currentPage.value = 1
}

const calculateStatistics = () => {
  const orders = salesOrders.value
  const today = new Date().toISOString().split('T')[0]

  salesStats.value = {
    totalOrders: orders.length,
    todayRevenue: orders
      .filter(order => order.sale_date === today && order.status === 'completed')
      .reduce((sum, order) => sum + parseFloat(order.total || 0), 0),
    pendingOrders: orders.filter(order => order.status === 'draft').length,
    cancelledOrders: orders.filter(order => order.status === 'cancelled').length
  }
}

const updateOrderStatus = async (order, newStatus) => {
  // Confirm action with user
  const statusText = {
    'confirmed': 'تایید',
    'cancelled': 'لغو',
    'completed': 'تکمیل'
  }

  const confirmMessage = `آیا از ${statusText[newStatus]} سفارش شماره ${order.invoice_number || order.id} اطمینان دارید؟`

  if (!confirm(confirmMessage)) {
    return
  }

  console.log('Updating order status:', { orderId: order.id, newStatus })

  const result = await salesStore.updateSalesOrderStatus(order.id, newStatus)

  if (result.success) {
    console.log('Status updated successfully')
    // Update statistics after status change
    calculateStatistics()
    // Success message
    showAlert('success', 'موفقیت', `وضعیت سفارش با موفقیت به "${statusText[newStatus]}" تغییر یافت`)
  } else {
    console.error('Status update failed:', result.error)
    showAlert('error', 'خطا در تغییر وضعیت', result.error)
  }
}

const refreshData = async () => {
  await salesStore.fetchSalesOrders()
}

const handleOrderSaved = async () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingOrder.value = null
  await refreshData()
  calculateStatistics()
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

    // Calculate statistics
    calculateStatistics()
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
