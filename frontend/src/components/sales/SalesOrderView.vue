<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center lg:justify-start bg-black bg-opacity-50 p-0 lg:p-4" @click.self="handleOverlayClick">
    <!-- Modal container - full screen on mobile, centered on desktop -->
    <div class="w-full h-full lg:w-auto lg:max-w-4xl lg:h-[85vh] rounded-lg bg-white dark:bg-black shadow-xl flex flex-col overflow-visible relative">

      <!-- Close button for large screens (top-left corner with blinking effect) -->
      <button @click="$emit('close')"
        class="hidden lg:block absolute -top-2 -left-2 z-50 rounded-full p-2 bg-red-500 text-white shadow-lg animate-pulse">
        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Header with mobile close button -->
      <div class="sticky top-0 z-20 bg-white border-b border-gray-200 px-4 py-3 lg:px-6 lg:py-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg lg:text-xl font-semibold text-gray-900">
              جزئیات سفارش فروش
            </h3>
            <p class="text-sm text-gray-500 mt-1">{{ salesOrder.invoice_number || 'در انتظار تولید' }}</p>
          </div>
          <div class="flex items-center gap-3">
            <!-- Status Badge -->
            <span :class="getStatusClass(salesOrder.status)"
              class="inline-flex rounded-full px-3 py-1 text-xs font-medium">
              {{ getStatusText(salesOrder.status) }}
            </span>

            <!-- Mobile close button -->
            <button @click="$emit('close')" class="lg:hidden rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto">
      <div class="p-6">
        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="space-y-4">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2">اطلاعات کلی</h4>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">شماره فاکتور:</label>
                <p class="text-gray-900 dark:text-white font-medium">{{ salesOrder.invoice_number }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500">تاریخ فروش:</label>
                <p class="text-gray-900 dark:text-white">{{ formatDate(salesOrder.sale_date) }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500">انبار:</label>
                <p class="text-gray-900 dark:text-white">{{ salesOrder.warehouse_name }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500">ایجاد شده توسط:</label>
                <p class="text-gray-900 dark:text-white">{{ salesOrder.created_by_name }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2">اطلاعات مشتری</h4>

            <div class="space-y-3">
              <div>
                <label class="text-sm font-medium text-gray-500">نام مشتری:</label>
                <p class="text-gray-900 dark:text-white font-medium">{{ salesOrder.customer_name }}</p>
              </div>

              <!-- Customer details would be loaded separately if needed -->
            </div>
          </div>
        </div>

        <!-- Items -->
        <div class="mb-8">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">آیتم‌های سفارش</h4>

          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">محصول</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">کد محصول</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">تعداد</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">قیمت واحد</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">تخفیف</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">جمع</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
                <tr v-for="item in salesOrder.items" :key="item.id">
                  <td class="px-4 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ item.product_name }}</div>
                    <div v-if="item.notes" class="text-sm text-gray-500">{{ item.notes }}</div>
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ item.product_code }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ formatNumber(item.quantity) }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ formatPrice(item.unit_price) }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ formatPrice(item.discount) }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    {{ formatPrice((item.quantity * item.unit_price) - item.discount) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Totals -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <!-- Notes -->
          <div v-if="salesOrder.notes">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">یادداشت</h4>
            <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <p class="text-gray-700 dark:text-gray-300">{{ salesOrder.notes }}</p>
            </div>
          </div>

          <!-- Financial Summary -->
          <div>
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">خلاصه مالی</h4>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">جمع کل:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatPrice(salesOrder.subtotal) }}</span>
              </div>

              <div v-if="salesOrder.discount_amount > 0" class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">تخفیف:</span>
                <span class="font-medium text-red-600">{{ formatPrice(salesOrder.discount_amount) }}</span>
              </div>

              <div v-if="salesOrder.tax_amount > 0" class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">مالیات:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatPrice(salesOrder.tax_amount) }}</span>
              </div>

              <div class="flex justify-between border-t pt-3">
                <span class="text-lg font-medium text-gray-900 dark:text-white">مبلغ نهایی:</span>
                <span class="text-lg font-bold text-gray-900 dark:text-white">{{ formatPrice(salesOrder.total) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Timeline/History -->
        <div class="mb-6">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">تاریخچه</h4>
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">ایجاد سفارش</p>
                <p class="text-xs text-gray-500">{{ formatDateTime(salesOrder.created_at) }}</p>
              </div>
            </div>

            <div v-if="salesOrder.updated_at !== salesOrder.created_at" class="flex items-center gap-3">
              <div class="w-2 h-2 bg-green-500 rounded-full"></div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">آخرین به‌روزرسانی</p>
                <p class="text-xs text-gray-500">{{ formatDateTime(salesOrder.updated_at) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 justify-end border-t pt-6">
          <button @click="$emit('close')"
            class="rounded-lg border border-gray-300 px-6 py-2 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700">
            بستن
          </button>

          <button v-if="salesOrder.status === 'draft'" @click="$emit('edit', salesOrder)"
            class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 transition-colors">
            ویرایش
          </button>

          <button v-if="canGenerateInvoice" @click="generateInvoice"
            class="rounded-lg bg-green-600 px-6 py-2 text-white hover:bg-green-700 transition-colors">
            صدور فاکتور
          </button>

          <button @click="printOrder"
            class="rounded-lg bg-gray-600 px-6 py-2 text-white hover:bg-gray-700 transition-colors">
            چاپ
          </button>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  salesOrder: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'edit'])

// Handle overlay click
const handleOverlayClick = () => {
  emit('close')
}

// Computed
const canGenerateInvoice = computed(() => {
  return ['confirmed', 'completed'].includes(props.salesOrder.status)
})

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const formatNumber = (number) => {
  if (!number) return '0'
  return new Intl.NumberFormat('fa-IR').format(number)
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR-u-ca-persian')
}

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('fa-IR-u-ca-persian')
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

const generateInvoice = () => {
  // TODO: Implement invoice generation
  alert('قابلیت صدور فاکتور به‌زودی اضافه خواهد شد')
}

const printOrder = () => {
  // TODO: Implement print functionality
  window.print()
}
</script>
