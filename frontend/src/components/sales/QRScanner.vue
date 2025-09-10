<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center overflow-y-auto z-99999">
    <div
      class="fixed inset-0 h-full w-full bg-gray-400/50 backdrop-blur-[32px]"
      aria-hidden="true"
      @click="$emit('close')"
    ></div>

    <!-- QR Scanner Modal -->
    <div class="relative w-full max-w-2xl mx-4 bg-white rounded-xl shadow-2xl dark:bg-gray-900">
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 rounded-t-xl">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          اسکن کد QR فاکتور
        </h3>
        <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Scanner Content -->
      <div class="p-6">
        <!-- Manual QR Input -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            یا کد QR را دستی وارد کنید:
          </label>
          <div class="flex gap-3">
            <input
              v-model="manualQRInput"
              type="text"
              placeholder="کد QR فاکتور را اینجا وارد کنید و PDF خودکار دانلود می‌شود..."
              class="flex-1 rounded-lg border-[1.5px] border-stroke bg-transparent py-3 px-4 text-black focus:border-primary focus-visible:outline-none dark:border-strokedark dark:bg-meta-4 dark:text-white dark:focus:border-primary"
              @keyup.enter="processQRCode(manualQRInput)"
            />
            <button
              @click="processQRCode(manualQRInput)"
              :disabled="!manualQRInput.trim()"
              class="inline-flex items-center justify-center rounded-md bg-primary px-6 py-3 text-center font-medium text-white hover:bg-opacity-90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              اسکن و دانلود PDF
            </button>
          </div>
        </div>

        <!-- QR Code Display Area -->
        <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
          <!-- Camera Scanner Placeholder -->
          <div v-if="!isCameraActive" class="mb-4">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
            </svg>
          </div>

          <!-- Camera Scanner UI (Placeholder) -->
          <div v-else class="mb-4">
            <div class="relative mx-auto h-48 w-64 bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden">
              <div class="absolute inset-0 flex items-center justify-center">
                <svg class="h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="absolute inset-0 border-4 border-transparent border-dashed"></div>
            </div>
            <button
              @click="toggleCamera"
              class="mt-4 inline-flex items-center justify-center rounded-md bg-gray-600 px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
            >
              غیرفعال کردن دوربین
            </button>
          </div>

          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">اسکن کد QR</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-4">
            کد QR فاکتور را وارد کنید - PDF رسید خودکار دانلود می‌شود
          </p>

          <button
            v-if="!isCameraActive"
            @click="toggleCamera"
            class="mt-2 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
          >
            فعال کردن دوربین
          </button>

          <!-- Sample QR Codes for Testing -->
          <div class="mt-6">
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">فاکتورهای ذخیره شده:</h4>
            <div class="grid grid-cols-1 gap-2 max-h-40 overflow-y-auto">
              <div
                v-for="invoice in storedInvoices"
                :key="invoice.qr_key || invoice.storage_key"
                class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div class="flex-1 text-right">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ invoice.invoice_number || 'در انتظار تولید' }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ invoice.customer_name }} - {{ formatPrice(invoice.total) }}
                  </p>
                </div>
                <button
                  @click="loadStoredInvoice(invoice)"
                  class="inline-flex items-center justify-center rounded-md bg-success px-3 py-1 text-xs font-medium text-white hover:bg-opacity-90 transition-colors"
                >
                  مشاهده
                </button>
              </div>
            </div>

            <div v-if="storedInvoices.length === 0" class="text-sm text-gray-500 dark:text-gray-400 py-4">
              هیچ فاکتور ذخیره شده‌ای یافت نشد
            </div>
          </div>
        </div>

        <!-- Result Display -->
        <div v-if="scannedInvoice" class="mt-6 p-4 rounded-lg" :class="{
          'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800': scannedInvoice.loading,
          'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800': scannedInvoice.success,
          'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800': scannedInvoice.error,
          'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800': !scannedInvoice.loading && !scannedInvoice.success && !scannedInvoice.error
        }">
          <div v-if="scannedInvoice.loading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <h4 class="text-lg font-medium text-blue-900 dark:text-blue-100">در حال تولید PDF رسید...</h4>
          </div>

          <div v-else-if="scannedInvoice.success" class="flex items-center">
            <svg class="h-5 w-5 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <h4 class="text-lg font-medium text-green-900 dark:text-green-100">PDF رسید با موفقیت دانلود شد!</h4>
          </div>

          <div v-else-if="scannedInvoice.error" class="flex items-center">
            <svg class="h-5 w-5 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            <h4 class="text-lg font-medium text-red-900 dark:text-red-100">خطا در تولید PDF</h4>
          </div>

          <div v-else>
            <h4 class="text-lg font-medium text-green-900 dark:text-green-100 mb-3">فاکتور یافت شد!</h4>
          </div>

          <div v-if="!scannedInvoice.loading" class="grid grid-cols-2 gap-4 text-sm mt-3">
            <div>
              <span class="text-gray-700 dark:text-gray-300">شماره فاکتور:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100 mr-2">{{ scannedInvoice.invoice_number }}</span>
            </div>
            <div>
              <span class="text-gray-700 dark:text-gray-300">مشتری:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100 mr-2">{{ scannedInvoice.customer_name }}</span>
            </div>
            <div>
              <span class="text-gray-700 dark:text-gray-300">مبلغ:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100 mr-2">{{ formatPrice(scannedInvoice.total) }}</span>
            </div>
            <div>
              <span class="text-gray-700 dark:text-gray-300">تاریخ:</span>
              <span class="font-medium text-gray-900 dark:text-gray-100 mr-2">{{ formatDate(scannedInvoice.sale_date) }}</span>
            </div>
          </div>

          <div class="flex gap-3 mt-4">
            <button
              @click="viewInvoiceDetails"
              class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
            >
              مشاهده جزئیات
            </button>
            <button
              @click="downloadPDFReceipt"
              class="inline-flex items-center justify-center rounded-md bg-success px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
            >
              دانلود PDF
            </button>
            <button
              @click="printReceipt"
              class="inline-flex items-center justify-center rounded-md bg-purple-600 px-4 py-2 text-center font-medium text-white hover:bg-opacity-90 transition-colors"
            >
              چاپ رسید
            </button>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="errorMessage" class="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <h4 class="text-lg font-medium text-red-900 dark:text-red-100 mb-2">خطا</h4>
          <p class="text-red-700 dark:text-red-300">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { getAllStoredInvoices, getInvoiceByQRCode, formatPrice, formatDate, retrieveStoredInvoice } from '@/utils/qrCodeUtils'
import { downloadReceiptPDF } from '@/utils/pdfUtils'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'invoice-found'])

// State
const manualQRInput = ref('')
const scannedInvoice = ref(null)
const errorMessage = ref('')
const isCameraActive = ref(false)
const autoCloseTimer = ref(null)

// Computed
const storedInvoices = computed(() => {
  return getAllStoredInvoices()
})

// Methods
const closeModal = () => {
  clearTimeout(autoCloseTimer.value)
  stopCamera()
  clearForm()
  emit('close')
}

const processQRCode = async (qrData) => {
  errorMessage.value = ''
  scannedInvoice.value = null

  if (!qrData || !qrData.trim()) {
    errorMessage.value = 'لطفاً کد QR را وارد کنید'
    return
  }

  console.log('Processing QR Code:', qrData) // Debug log

  let invoice = null

  // Check if it's a URL (new mobile format)
  if (qrData.startsWith('http://') || qrData.startsWith('https://')) {
    console.log('Detected URL format QR code') // Debug log

    // Extract invoice key from URL
    const urlParts = qrData.split('/mobile-receipt/')
    if (urlParts.length === 2) {
      const invoiceKey = urlParts[1]
      console.log('Extracted invoice key:', invoiceKey) // Debug log

      // Retrieve invoice from localStorage
      invoice = retrieveStoredInvoice(invoiceKey)
      console.log('Retrieved invoice from storage:', invoice) // Debug log
    }
  } else {
    // Try old JSON format for backward compatibility
    console.log('Trying JSON format QR code') // Debug log
    invoice = getInvoiceByQRCode(qrData)
  }

  if (invoice) {
    console.log('Invoice found:', invoice) // Debug log
    scannedInvoice.value = invoice

    // Show success message immediately
    errorMessage.value = ''

    try {
      // Show temporary success message
      scannedInvoice.value = { ...invoice, loading: true }

      // Automatically download PDF receipt
      console.log('Starting PDF download...') // Debug log
      const result = await downloadReceiptPDF(invoice)
      console.log('PDF download result:', result) // Debug log

      if (result.success) {
        // Show success message
        scannedInvoice.value = { ...invoice, success: true }

        // Close scanner after successful download
        autoCloseTimer.value = setTimeout(() => {
          emit('close')
        }, 3000) // Give more time to see success message
      } else {
        errorMessage.value = 'خطا در تولید PDF: ' + (result.error || 'خطای نامشخص')
        scannedInvoice.value = { ...invoice, error: true }
      }
    } catch (error) {
      console.error('Error downloading PDF:', error)
      errorMessage.value = 'خطا در دانلود PDF رسید: ' + error.message
      scannedInvoice.value = { ...invoice, error: true }
    }
  } else {
    console.log('Invoice not found for QR data:', qrData) // Debug log
    errorMessage.value = 'کد QR نامعتبر است یا فاکتور یافت نشد'
  }
}

const loadStoredInvoice = (invoice) => {
  scannedInvoice.value = invoice
  errorMessage.value = ''
}

const viewInvoiceDetails = () => {
  if (scannedInvoice.value) {
    emit('invoice-found', scannedInvoice.value)
    closeModal()
  }
}

const downloadPDFReceipt = async () => {
  if (scannedInvoice.value) {
    try {
      const result = await downloadReceiptPDF(scannedInvoice.value)

      if (result.success) {
        // Show success message or close modal
        setTimeout(() => {
          emit('close')
        }, 1000)
      } else {
        errorMessage.value = 'خطا در تولید PDF: ' + result.error
      }
    } catch (error) {
      console.error('Error downloading PDF:', error)
      errorMessage.value = 'خطا در دانلود PDF رسید'
    }
  }
}

const printInvoice = () => {
  if (scannedInvoice.value) {
    const printWindow = window.open('', '_blank')
    const receiptHTML = generateReceiptHTML(scannedInvoice.value)

    printWindow.document.write(receiptHTML)
    printWindow.document.close()
    printWindow.print()
  }
}

const printReceipt = () => {
  if (scannedInvoice.value) {
    const printWindow = window.open('', '_blank')
    const receiptHTML = generateReceiptWithQRHTML(scannedInvoice.value)

    printWindow.document.write(receiptHTML)
    printWindow.document.close()
    printWindow.print()

    // Close the scanner modal after printing
    closeModal()
  }
}

const toggleCamera = () => {
  isCameraActive.value = !isCameraActive.value
  if (isCameraActive.value) {
    startCamera()
  } else {
    stopCamera()
  }
}

const startCamera = () => {
  // Placeholder for camera initialization
  console.log('Camera started - this would initialize the QR scanner')
  // In a real implementation, this would:
  // 1. Request camera permissions
  // 2. Initialize a QR scanner library like jsQR or Instascan
  // 3. Set up video element and processing loop
}

const stopCamera = () => {
  // Placeholder for camera cleanup
  console.log('Camera stopped - this would clean up the QR scanner')
  // In a real implementation, this would:
  // 1. Stop the video stream
  // 2. Clean up any scanner intervals
  // 3. Release camera resources
}

const generateReceiptHTML = (invoice) => {
  // Escape HTML to prevent XSS
  const escapeHTML = (str) => {
    if (!str) return ''
    return str
      .toString()
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;')
  }

  const invoiceNumber = escapeHTML(invoice.invoice_number)
  const customerName = escapeHTML(invoice.customer_name)
  const saleDate = escapeHTML(formatDate(invoice.sale_date))
  const total = escapeHTML(formatPrice(invoice.total))

  const itemsHTML = invoice.items ? invoice.items.map(item => `
    <tr>
      <td>${escapeHTML(item.product_name)}</td>
      <td>${escapeHTML(item.quantity)}</td>
      <td>${escapeHTML(formatPrice(item.unit_price))}</td>
      <td>${escapeHTML(formatPrice((item.quantity * item.unit_price) - (item.discount || 0)))}</td>
    </tr>
  `).join('') : '<tr><td colspan="4">اطلاعات آیتم‌ها در دسترس نیست</td></tr>'

  return `
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
      <meta charset="UTF-8">
      <title>رسید فروش - ${invoiceNumber}</title>
      <style>
        body { font-family: 'Tahoma', sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .info { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .items { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        .items th, .items td { border: 1px solid #ddd; padding: 8px; text-align: right; }
        .items th { background-color: #f5f5f5; }
        .total { text-align: right; font-weight: bold; font-size: 18px; }
        @media print { body { margin: 0; } }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>یراقالات ناصری</h1>
        <h2>رسید فروش</h2>
      </div>

      <div class="info">
        <div>
          <strong>شماره فاکتور:</strong> ${invoiceNumber || 'در انتظار تولید'}<br>
          <strong>تاریخ:</strong> ${saleDate}<br>
        </div>
        <div>
          <strong>مشتری:</strong> ${customerName}<br>
        </div>
      </div>

      <table class="items">
        <thead>
          <tr>
            <th>محصول</th>
            <th>تعداد</th>
            <th>قیمت واحد</th>
            <th>جمع</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHTML}
        </tbody>
      </table>

      <div class="total">
        مبلغ نهایی: ${total}
      </div>

      <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #666;">
        تاریخ چاپ: ${new Date().toLocaleString('fa-IR')}<br>
        سیستم مدیریت یراقالات ناصری
      </div>
    </body>
    </html>
  `
}

const generateReceiptWithQRHTML = (invoice) => {
  // Escape HTML to prevent XSS
  const escapeHTML = (str) => {
    if (!str) return ''
    return str
      .toString()
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;')
  }

  // Generate QR code data
  const qrData = JSON.stringify({
    id: invoice.id,
    invoice_number: invoice.invoice_number,
    customer_name: invoice.customer_name,
    total: invoice.total,
    sale_date: invoice.sale_date,
    status: invoice.status,
    storage_key: invoice.qr_key || invoice.storage_key,
    app_name: 'Yaraghalat_Naseri_ERP'
  })

  const invoiceNumber = escapeHTML(invoice.invoice_number)
  const customerName = escapeHTML(invoice.customer_name)
  const saleDate = escapeHTML(formatDate(invoice.sale_date))
  const total = escapeHTML(formatPrice(invoice.total))

  const itemsHTML = invoice.items ? invoice.items.map(item => `
    <tr>
      <td>${escapeHTML(item.product_name)}</td>
      <td>${escapeHTML(item.quantity)}</td>
      <td>${escapeHTML(formatPrice(item.unit_price))}</td>
      <td>${escapeHTML(formatPrice((item.quantity * item.unit_price) - (item.discount || 0)))}</td>
    </tr>
  `).join('') : '<tr><td colspan="4">اطلاعات آیتم‌ها در دسترس نیست</td></tr>'

  return `
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
      <meta charset="UTF-8">
      <title>رسید فروش - ${invoiceNumber}</title>
      <style>
        body { font-family: 'Tahoma', sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .info { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .items { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        .items th, .items td { border: 1px solid #ddd; padding: 8px; text-align: right; }
        .items th { background-color: #f5f5f5; }
        .total { text-align: right; font-weight: bold; font-size: 18px; margin-bottom: 20px; }
        .qr-section { text-align: center; margin: 20px 0; }
        .qr-code { display: inline-block; border: 2px solid #000; padding: 10px; }
        @media print { body { margin: 0; } }
      </style>
      <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"><\/script>
    </head>
    <body>
      <div class="header">
        <h1>یراقالات ناصری</h1>
        <h2>رسید فروش</h2>
      </div>

      <div class="info">
        <div>
          <strong>شماره فاکتور:</strong> ${invoiceNumber || 'در انتظار تولید'}<br>
          <strong>تاریخ:</strong> ${saleDate}<br>
        </div>
        <div>
          <strong>مشتری:</strong> ${customerName}<br>
        </div>
      </div>

      <table class="items">
        <thead>
          <tr>
            <th>محصول</th>
            <th>تعداد</th>
            <th>قیمت واحد</th>
            <th>جمع</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHTML}
        </tbody>
      </table>

      <div class="total">
        مبلغ نهایی: ${total}
      </div>

      <div class="qr-section">
        <div class="qr-code">
          <canvas id="qrcode"></canvas>
        </div>
        <p style="margin-top: 10px; font-size: 12px;">کد QR برای دسترسی آفلاین به فاکتور</p>
      </div>

      <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #666;">
        تاریخ چاپ: ${new Date().toLocaleString('fa-IR')}<br>
        سیستم مدیریت یراقالات ناصری
      </div>

      <script>
        // Generate QR code when page loads
        window.onload = function() {
          const canvas = document.getElementById('qrcode');
          const qrData = ${JSON.stringify(qrData)};
          QRCode.toCanvas(canvas, qrData, {
            width: 150,
            margin: 2,
            color: {
              dark: '#000000',
              light: '#FFFFFF'
            }
          }, function (error) {
            if (error) console.error(error);
            // Auto print after QR code is generated
            setTimeout(() => {
              window.print();
            }, 500);
          });
        };
      <\/script>
    </body>
    </html>
  `
}

// Clear form when modal closes
const clearForm = () => {
  manualQRInput.value = ''
  scannedInvoice.value = null
  errorMessage.value = ''
  stopCamera()
  isCameraActive.value = false
}

// Watch for modal visibility changes
watch(() => props.show, (newVal) => {
  if (!newVal) {
    clearForm()
  }
})

// Clean up on component unmount
onUnmounted(() => {
  clearTimeout(autoCloseTimer.value)
  stopCamera()
})
</script>
