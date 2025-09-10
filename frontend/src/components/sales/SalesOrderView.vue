<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center overflow-y-auto z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>

    <!-- Modal Body -->
    <div class="relative w-full max-w-4xl mx-4 bg-white rounded-xl shadow-2xl dark:bg-gray-900 max-h-[90vh] overflow-y-auto">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-t-xl">
        <div class="flex items-center gap-4">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            جزئیات سفارش فروش
          </h3>
          <!-- Status Badge -->
          <span :class="getStatusClass(salesOrder.status)"
            class="inline-flex rounded-full px-3 py-1 text-xs font-medium">
            {{ getStatusText(salesOrder.status) }}
          </span>
        </div>
        <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Content -->
      <div class="p-6">
        <!-- Invoice Number Display -->
        <div class="mb-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">شماره فاکتور:</p>
          <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ salesOrder.invoice_number || 'در انتظار تولید' }}</p>
        </div>

        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="space-y-4">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2">اطلاعات کلی</h4>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">شماره فاکتور:</label>
                <p class="text-gray-900 dark:text-white font-medium">{{ salesOrder.invoice_number || 'در انتظار تولید' }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">تاریخ فروش:</label>
                <p class="text-gray-900 dark:text-white">{{ formatDate(salesOrder.sale_date) }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">انبار:</label>
                <p class="text-gray-900 dark:text-white">{{ salesOrder.warehouse_name }}</p>
              </div>

              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">ایجاد شده توسط:</label>
                <p class="text-gray-900 dark:text-white">{{ salesOrder.created_by_name }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2">اطلاعات مشتری</h4>

            <div class="space-y-3">
              <div>
                <label class="text-sm font-medium text-gray-500 dark:text-gray-400">نام مشتری:</label>
                <p class="text-gray-900 dark:text-white font-medium">{{ salesOrder.customer_name }}</p>
              </div>

              <!-- Customer details would be loaded separately if needed -->
            </div>
          </div>
        </div>

        <!-- Items -->
        <div class="mb-8">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">آیتم‌های سفارش</h4>

          <div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-gray-800">
            <div class="max-w-full overflow-x-auto">
              <table class="w-full table-auto">
                <thead>
                  <tr class="border-b border-[#eee] bg-gray-2 text-right dark:bg-gray-800">
                    <th class="min-w-[150px] px-4 py-4 font-medium text-black dark:text-white">محصول</th>
                    <th class="min-w-[120px] px-4 py-4 font-medium text-black dark:text-white">کد محصول</th>
                    <th class="min-w-[80px] px-4 py-4 font-medium text-black dark:text-white">تعداد</th>
                    <th class="min-w-[100px] px-4 py-4 font-medium text-black dark:text-white">قیمت واحد</th>
                    <th class="min-w-[80px] px-4 py-4 font-medium text-black dark:text-white">تخفیف</th>
                    <th class="min-w-[100px] px-4 py-4 font-medium text-black dark:text-white">جمع</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in salesOrder.items" :key="item.id"
                    class="border-b border-[#eee] dark:border-strokedark">
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <div class="text-black dark:text-white font-medium">{{ item.product_name }}</div>
                      <div v-if="item.notes" class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ item.notes }}</div>
                    </td>
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <p class="text-black dark:text-white">{{ item.product_code }}</p>
                    </td>
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <p class="text-black dark:text-white">{{ formatNumber(item.quantity) }}</p>
                    </td>
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <p class="text-black dark:text-white">{{ formatPrice(item.unit_price) }}</p>
                    </td>
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <p class="text-black dark:text-white">{{ formatPrice(item.discount) }}</p>
                    </td>
                    <td class="border-b border-[#eee] px-4 py-5 dark:border-strokedark">
                      <p class="text-black dark:text-white font-medium">{{ formatPrice((item.quantity * item.unit_price) - item.discount) }}</p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Totals -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <!-- Notes -->
          <div v-if="salesOrder.notes">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">یادداشت</h4>
            <div class="rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-gray-800">
              <p class="text-gray-700 dark:text-gray-300">{{ salesOrder.notes }}</p>
            </div>
          </div>

          <!-- Financial Summary -->
          <div>
            <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">خلاصه مالی</h4>
            <div class="rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-gray-800">
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
        </div>

        <!-- Timeline/History -->
        <div class="mb-6">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white border-b pb-2 mb-4">تاریخچه</h4>
          <div class="rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-gray-800">
            <div class="space-y-3">
              <div class="flex items-center gap-3">
                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">ایجاد سفارش</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDateTime(salesOrder.created_at) }}</p>
                </div>
              </div>

              <div v-if="salesOrder.updated_at !== salesOrder.created_at" class="flex items-center gap-3">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">آخرین به‌روزرسانی</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDateTime(salesOrder.updated_at) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 justify-start border-t pt-6">
          <button @click="$emit('close')"
            class="inline-flex items-center justify-center rounded-md border-[1.5px] border-gray-200 bg-gray-100 px-6 py-3 text-center font-medium text-dark hover:bg-gray-200 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600 transition-colors">
            بستن
          </button>

          <button v-if="salesOrder.status === 'draft'" @click="$emit('edit', salesOrder)"
            class="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-center font-medium text-white hover:bg-opacity-90 transition-colors">
            ویرایش
          </button>

          <button v-if="canGenerateInvoice" @click="generateInvoice"
            class="inline-flex items-center justify-center rounded-md bg-success px-6 py-3 text-center font-medium text-white hover:bg-opacity-90 transition-colors">
            صدور فاکتور
          </button>

          <button @click="printOrder"
            class="inline-flex items-center justify-center rounded-md bg-gray-800 px-6 py-3 text-center font-medium text-white hover:bg-opacity-90 transition-colors">
            چاپ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  salesOrder: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'edit'])

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
    'draft': 'bg-gray-50 text-gray-700 dark:bg-gray-500/15 dark:text-gray-500',
    'confirmed': 'bg-blue-50 text-blue-700 dark:bg-blue-500/15 dark:text-blue-500',
    'completed': 'bg-success-50 text-success-700 dark:bg-success-500/15 dark:text-success-500',
    'cancelled': 'bg-error-50 text-error-700 dark:bg-error-500/15 dark:text-error-500'
  }
  return classMap[status] || 'bg-gray-50 text-gray-700 dark:bg-gray-500/15 dark:text-gray-500'
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
