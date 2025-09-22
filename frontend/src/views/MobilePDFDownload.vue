<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <!-- Header -->
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">یراقالات ناصری</h1>
        <p class="text-gray-600 dark:text-gray-400">دانلود رسید فروش</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <div class="inline-flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-lg text-gray-700 dark:text-gray-300">در حال آماده‌سازی رسید...</span>
        </div>
      </div>

      <!-- Success State -->
      <div v-else-if="success && invoice" class="text-center py-4">
        <div class="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">رسید آماده است!</h2>

        <!-- Invoice Details -->
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6 text-right">
          <div class="grid grid-cols-1 gap-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">شماره فاکتور:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ invoice.invoice_number || 'در انتظار تولید' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">مشتری:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ invoice.customer_name || 'نامشخص' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">مبلغ:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ formatPrice(invoice.total) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">تاریخ:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(invoice.sale_date) }}</span>
            </div>
          </div>
        </div>

        <!-- Download Button -->
        <button
          @click="downloadPDF"
          :disabled="downloading"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center"
        >
          <svg v-if="downloading" class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          {{ downloading ? 'در حال دانلود...' : 'دانلود رسید PDF' }}
        </button>

        <!-- Alternative Actions -->
        <div class="mt-4 space-y-2">
          <button
            @click="viewInBrowser"
            class="w-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg transition-colors"
          >
            مشاهده در مرورگر
          </button>

          <!-- Mobile-specific instructions -->
          <div v-if="isMobile" class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <p class="text-xs text-blue-700 dark:text-blue-300 text-center">
              📱 در صورت عدم دانلود خودکار، روی دکمه "دانلود رسید PDF" کلیک کنید
            </p>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">خطا در بارگذاری</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-4">{{ errorMessage }}</p>
        <button
          @click="retry"
          class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
        >
          تلاش مجدد
        </button>
      </div>

      <!-- Footer -->
      <div class="text-center mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
        <p class="text-xs text-gray-500 dark:text-gray-400">
          سیستم مدیریت یراقالات ناصری
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { retrieveStoredInvoice } from '@/utils/qrCodeUtils'
import { downloadReceiptPDF, loadPersianFonts } from '@/utils/pdfUtilsFixed'

// Route
const route = useRoute()

// State
const loading = ref(true)
const success = ref(false)
const error = ref(false)
const downloading = ref(false)
const errorMessage = ref('')
const invoice = ref(null)
const isMobile = ref(false)

// Detect mobile device
const detectMobile = () => {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera
  isMobile.value = /android|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent.toLowerCase())
}

// Methods
const formatPrice = (price) => {
  if (!price) return '0 تومان'
  return new Intl.NumberFormat('fa-IR').format(price) + ' تومان'
}

const formatDate = (dateString) => {
  if (!dateString) return 'نامشخص'
  try {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('fa-IR').format(date)
  } catch (error) {
    return 'نامشخص'
  }
}

const loadInvoice = async () => {
  try {
    loading.value = true
    error.value = false
    
    // Load Persian fonts for proper PDF generation
    await loadPersianFonts()

    const invoiceKey = route.params.invoiceKey

    if (!invoiceKey) {
      throw new Error('کلید فاکتور نامعتبر است')
    }

    // Try to retrieve from localStorage
    const storedInvoice = retrieveStoredInvoice(invoiceKey)

    if (!storedInvoice) {
      throw new Error('فاکتور یافت نشد. ممکن است منقضی شده باشد.')
    }

    invoice.value = storedInvoice
    success.value = true

    // Auto-download PDF after a short delay for better UX
    // On mobile devices, wait a bit longer to show the interface
    const delay = isMobile.value ? 2500 : 1500
    setTimeout(() => {
      downloadPDF()
    }, delay)

  } catch (err) {
    console.error('Error loading invoice:', err)
    error.value = true
    errorMessage.value = err.message || 'خطا در بارگذاری فاکتور'
  } finally {
    loading.value = false
  }
}

const downloadPDF = async () => {
  if (!invoice.value) return

  try {
    downloading.value = true
    const result = await downloadReceiptPDF(invoice.value)

    if (!result.success) {
      throw new Error(result.error || 'خطا در تولید PDF')
    }

    // Show success message
    alert('رسید با موفقیت دانلود شد!')

  } catch (err) {
    console.error('Error downloading PDF:', err)
    alert('خطا در دانلود PDF: ' + err.message)
  } finally {
    downloading.value = false
  }
}

const viewInBrowser = () => {
  // Open the receipt in a new window/tab for viewing
  if (invoice.value) {
    const receiptWindow = window.open('', '_blank')
    receiptWindow.document.write(generateReceiptHTML())
    receiptWindow.document.close()
  }
}

const generateReceiptHTML = () => {
  if (!invoice.value) return ''

  return `
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>رسید فروش - ${invoice.value.invoice_number}</title>
      <style>
        body { font-family: Tahoma, Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .receipt { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        .header { text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 20px; }
        .company-name { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 5px; }
        .receipt-title { font-size: 18px; color: #666; }
        .details { margin: 20px 0; }
        .detail-row { display: flex; justify-content: space-between; margin: 10px 0; padding: 5px 0; border-bottom: 1px dotted #ccc; }
        .items { margin: 20px 0; }
        .items-header { background: #f8f9fa; padding: 10px; font-weight: bold; border-radius: 5px; }
        .item { padding: 10px; border-bottom: 1px solid #eee; }
        .total { font-size: 18px; font-weight: bold; text-align: center; background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; color: #666; font-size: 12px; }
      </style>
    </head>
    <body>
      <div class="receipt">
        <div class="header">
          <div class="company-name">یراقالات ناصری</div>
          <div class="receipt-title">رسید فروش</div>
        </div>

        <div class="details">
          <div class="detail-row">
            <span>شماره فاکتور:</span>
            <span>${invoice.value.invoice_number || 'در انتظار تولید'}</span>
          </div>
          <div class="detail-row">
            <span>مشتری:</span>
            <span>${invoice.value.customer_name || 'نامشخص'}</span>
          </div>
          <div class="detail-row">
            <span>تاریخ:</span>
            <span>${formatDate(invoice.value.sale_date)}</span>
          </div>
        </div>

        <div class="items">
          <div class="items-header">محصولات:</div>
          ${invoice.value.items && invoice.value.items.length > 0
            ? invoice.value.items.map((item, index) => `
              <div class="item">
                ${index + 1}. ${item.product_name || 'محصول نامشخص'} -
                تعداد: ${item.quantity || 0} -
                قیمت: ${formatPrice(item.unit_price || 0)}
              </div>
            `).join('')
            : '<div class="item">اطلاعات آیتم‌ها در دسترس نیست</div>'
          }
        </div>

        <div class="total">
          مبلغ نهایی: ${formatPrice(invoice.value.total)}
        </div>

        <div class="footer">
          <p>تاریخ چاپ: ${formatDate(new Date().toISOString())}</p>
          <p>سیستم مدیریت یراقالات ناصری</p>
        </div>
      </div>
    </body>
    </html>
  `
}

const retry = () => {
  loadInvoice()
}

// Lifecycle
onMounted(() => {
  detectMobile()
  loadInvoice()
})
</script>

<style scoped>
/* Additional mobile-specific styles */
@media (max-width: 640px) {
  .max-w-md {
    max-width: 100%;
    margin: 0;
    border-radius: 0;
  }
}
</style>
