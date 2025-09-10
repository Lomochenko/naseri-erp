<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center overflow-y-auto z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>

    <!-- Receipt Modal -->
    <div class="relative w-full max-w-4xl mx-4 bg-white rounded-xl shadow-2xl dark:bg-gray-900 max-h-[90vh] overflow-y-auto">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-t-xl">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          رسید فروش
        </h3>
        <div class="flex items-center gap-3">
          <button @click="downloadPDF"
            class="inline-flex items-center justify-center rounded-md bg-success px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            دانلود PDF
          </button>
          <button @click="printReceipt"
            class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            چاپ رسید
          </button>
          <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Receipt Content -->
      <div id="receipt-content" class="p-8 bg-white dark:bg-gray-900">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">یراقالات ناصری</h1>
          <p class="text-gray-600 dark:text-gray-400">رسید فروش</p>
        </div>

        <!-- Invoice Info -->
        <div class="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">اطلاعات فاکتور</h3>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">شماره فاکتور:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ salesOrder.invoice_number || 'در انتظار تولید' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">تاریخ:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(salesOrder.sale_date) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">وضعیت:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ getStatusText(salesOrder.status) }}</span>
              </div>
            </div>
          </div>

          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">اطلاعات مشتری</h3>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">نام مشتری:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ salesOrder.customer_name }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Items Table -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">آیتم‌های سفارش</h3>
          <div class="overflow-x-auto">
            <table class="w-full border-collapse border border-gray-300 dark:border-gray-600">
              <thead>
                <tr class="bg-gray-50 dark:bg-gray-800">
                  <th class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-right font-medium text-gray-900 dark:text-white">محصول</th>
                  <th class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-right font-medium text-gray-900 dark:text-white">تعداد</th>
                  <th class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-right font-medium text-gray-900 dark:text-white">قیمت واحد</th>
                  <th class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-right font-medium text-gray-900 dark:text-white">تخفیف</th>
                  <th class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-right font-medium text-gray-900 dark:text-white">جمع</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in salesOrder.items" :key="item.id">
                  <td class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-gray-900 dark:text-white">
                    {{ item.product_name }}
                    <div v-if="item.notes" class="text-sm text-gray-500 dark:text-gray-400">{{ item.notes }}</div>
                  </td>
                  <td class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-gray-900 dark:text-white">{{ formatNumber(item.quantity) }}</td>
                  <td class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-gray-900 dark:text-white">{{ formatPrice(item.unit_price) }}</td>
                  <td class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-gray-900 dark:text-white">{{ formatPrice(item.discount) }}</td>
                  <td class="border border-gray-300 dark:border-gray-600 px-4 py-2 text-gray-900 dark:text-white font-medium">{{ formatPrice((item.quantity * item.unit_price) - item.discount) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Totals and QR Code -->
        <div class="grid grid-cols-2 gap-8 mb-8">
          <!-- Financial Summary -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">خلاصه مالی</h3>
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
                <span class="text-lg font-bold text-gray-900 dark:text-white">مبلغ نهایی:</span>
                <span class="text-lg font-bold text-gray-900 dark:text-white">{{ formatPrice(salesOrder.total) }}</span>
              </div>
            </div>
          </div>

          <!-- QR Code -->
          <div class="flex flex-col items-center">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">کد QR فاکتور</h3>
            <div class="bg-white p-4 rounded-lg shadow-md">
              <QRCodeVue3
                :width="150"
                :height="150"
                :value="qrCodeData"
                :qrOptions="{ typeNumber: 0, mode: 'Byte', errorCorrectionLevel: 'M' }"
                :imageOptions="{ hideBackgroundDots: true, imageSize: 0.4, margin: 0 }"
                :dotsOptions="{ type: 'rounded', color: '#000000' }"
                :backgroundOptions="{ color: '#ffffff' }"
                :cornersSquareOptions="{ type: 'extra-rounded', color: '#000000' }"
                :cornersDotOptions="{ type: 'dot', color: '#000000' }"
              />
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
              اسکن کنید برای دریافت فاکتور
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="text-center text-sm text-gray-500 dark:text-gray-400 border-t pt-4">
          <p>تاریخ چاپ: {{ formatDateTime(new Date()) }}</p>
          <p class="mt-1">سیستم مدیریت یراقالات ناصری</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import QRCodeVue3 from 'qrcode-vue3'
import { downloadReceiptPDF } from '@/utils/pdfUtils'
import { generateQRCodeData, storeInvoiceOffline, generateMobileQRCodeURL } from '@/utils/qrCodeUtils'

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

const emit = defineEmits(['close'])

// Computed
const qrCodeData = computed(() => {
  // Generate mobile-compatible URL for QR code
  return generateMobileQRCodeURL(props.salesOrder)
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

const printReceipt = () => {
  // Store original styles
  const originalStyles = document.head.innerHTML

  // Create print-specific styles
  const printStyles = `
    <style>
      @media print {
        body * { visibility: hidden; }
        #receipt-content, #receipt-content * { visibility: visible; }
        #receipt-content {
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
          background: white !important;
          color: black !important;
        }
        .dark\\:bg-gray-900 { background: white !important; }
        .dark\\:text-white { color: black !important; }
        .dark\\:text-gray-400 { color: #666 !important; }
        .dark\\:border-gray-600 { border-color: #ccc !important; }
        .dark\\:bg-gray-800 { background: #f5f5f5 !important; }
      }
    </style>
  `

  // Add print styles
  document.head.insertAdjacentHTML('beforeend', printStyles)

  // Print
  window.print()

  // Clean up - remove print styles after printing
  setTimeout(() => {
    const printStyleElements = document.querySelectorAll('style')
    printStyleElements.forEach(style => {
      if (style.innerHTML.includes('@media print')) {
        style.remove()
      }
    })
  }, 1000)
}

const downloadPDF = async () => {
  try {
    const result = await downloadReceiptPDF(props.salesOrder)

    if (!result.success) {
      alert('خطا در تولید PDF: ' + result.error)
    }
    // If successful, the PDF will be automatically downloaded
  } catch (error) {
    console.error('Error downloading PDF:', error)
    alert('خطا در دانلود PDF رسید')
  }
}
</script>

<style scoped>
@media print {
  .fixed, .backdrop-blur-\\[32px\\] {
    display: none !important;
  }
}
</style>
