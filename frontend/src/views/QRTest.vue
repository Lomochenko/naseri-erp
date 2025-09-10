<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-6">QR Code Test Page</h1>

    <!-- Test Invoice Data -->
    <div class="mb-8 p-6 bg-gray-50 rounded-lg">
      <h2 class="text-lg font-semibold mb-4">Test Invoice Data</h2>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <strong>Invoice Number:</strong> INV-2025-001
        </div>
        <div>
          <strong>Customer:</strong> احمد محمدی
        </div>
        <div>
          <strong>Total:</strong> 1,250,000 تومان
        </div>
        <div>
          <strong>Date:</strong> {{ new Date().toLocaleDateString('fa-IR') }}
        </div>
      </div>
    </div>

    <!-- Generate QR Code -->
    <div class="mb-8 flex gap-4">
      <button
        @click="generateTestQR"
        class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
      >
        Generate Test QR Code
      </button>
      <button
        @click="testPDFDownload"
        class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700"
      >
        Test PDF Download
      </button>
      <button
        @click="generateMobileQR"
        class="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
      >
        Generate Mobile QR URL
      </button>
      <button
        @click="testMobileWorkflow"
        class="bg-orange-600 text-white px-6 py-3 rounded-lg hover:bg-orange-700"
      >
        Test Mobile Workflow
      </button>
    </div>

    <!-- Display QR Code -->
    <div v-if="qrCodeData" class="mb-8 p-6 bg-white border rounded-lg">
      <h3 class="text-lg font-semibold mb-4">Generated QR Code</h3>
      <div class="flex items-start gap-6">
        <div class="bg-white p-4 border rounded">
          <QRCodeVue3
            :width="200"
            :height="200"
            :value="qrCodeData"
            :qrOptions="{ typeNumber: 0, mode: 'Byte', errorCorrectionLevel: 'M' }"
            :imageOptions="{ hideBackgroundDots: true, imageSize: 0.4, margin: 0 }"
            :dotsOptions="{ type: 'rounded', color: '#000000' }"
            :backgroundOptions="{ color: '#ffffff' }"
            :cornersSquareOptions="{ type: 'extra-rounded', color: '#000000' }"
            :cornersDotOptions="{ type: 'dot', color: '#000000' }"
          />
        </div>
        <div class="flex-1">
          <h4 class="font-semibold mb-2">QR Code Data:</h4>
          <pre class="bg-gray-100 p-3 rounded text-sm overflow-auto">{{ qrCodeData }}</pre>
          <button
            @click="copyToClipboard"
            class="mt-2 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Copy QR Data
          </button>
        </div>
      </div>
    </div>

    <!-- Test QR Scanner -->
    <div class="mb-8">
      <h3 class="text-lg font-semibold mb-4">Test QR Scanner</h3>
      <div class="flex gap-4 mb-4">
        <input
          v-model="testQRInput"
          type="text"
          placeholder="Paste QR code data here to test..."
          class="flex-1 border rounded px-4 py-2"
        />
        <button
          @click="testQRScan"
          class="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
        >
          Test Scan
        </button>
      </div>
      <div class="flex gap-4">
        <button
          @click="testQRScanWithPDF"
          class="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700"
        >
          Test QR Scan + Auto PDF
        </button>
      </div>
    </div>

    <!-- Scan Results -->
    <div v-if="scanResult" class="mb-8 p-6 bg-green-50 border border-green-200 rounded-lg">
      <h3 class="text-lg font-semibold mb-4 text-green-800">Scan Result</h3>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <strong>Invoice Number:</strong> {{ scanResult.invoice_number }}
        </div>
        <div>
          <strong>Customer:</strong> {{ scanResult.customer_name }}
        </div>
        <div>
          <strong>Total:</strong> {{ formatPrice(scanResult.total) }}
        </div>
        <div>
          <strong>Status:</strong> {{ scanResult.status }}
        </div>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="errorMessage" class="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-red-800">{{ errorMessage }}</p>
    </div>

    <!-- Stored Invoices -->
    <div class="mb-8">
      <h3 class="text-lg font-semibold mb-4">Stored Invoices (LocalStorage)</h3>
      <div class="space-y-2">
        <div
          v-for="invoice in storedInvoices"
          :key="invoice.qr_key"
          class="p-4 bg-gray-50 border rounded flex justify-between items-center"
        >
          <div>
            <strong>{{ invoice.invoice_number }}</strong> - {{ invoice.customer_name }}
            <br>
            <small class="text-gray-600">{{ formatPrice(invoice.total) }} - {{ formatDate(invoice.sale_date) }}</small>
          </div>
          <button
            @click="loadInvoice(invoice)"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Load
          </button>
        </div>
        <div v-if="storedInvoices.length === 0" class="text-gray-500 text-center py-4">
          No stored invoices found
        </div>
      </div>
    </div>

    <!-- Clear Storage -->
    <div class="mb-8">
      <button
        @click="clearStorage"
        class="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700"
      >
        Clear All Stored Invoices
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import QRCodeVue3 from 'qrcode-vue3'
import {
  generateQRCodeData,
  storeInvoiceOffline,
  getAllStoredInvoices,
  getInvoiceByQRCode,
  formatPrice,
  formatDate
} from '@/utils/qrCodeUtils'
import { downloadReceiptPDF } from '@/utils/pdfUtils'
import { generateMobileQRCodeURL } from '@/utils/qrCodeUtils'

// State
const qrCodeData = ref('')
const testQRInput = ref('')
const scanResult = ref(null)
const errorMessage = ref('')

// Test invoice data
const testInvoice = {
  id: Math.floor(Math.random() * 1000),
  invoice_number: 'INV-2025-001',
  customer_name: 'احمد محمدی',
  total: 1250000,
  sale_date: new Date().toISOString().split('T')[0],
  status: 'completed',
  items: [
    {
      id: 1,
      product_name: 'پیچ و مهره',
      quantity: 10,
      unit_price: 50000,
      discount: 0
    },
    {
      id: 2,
      product_name: 'قفل درب',
      quantity: 2,
      unit_price: 350000,
      discount: 0
    }
  ]
}

// Computed
const storedInvoices = computed(() => {
  return getAllStoredInvoices()
})

// Methods
const generateTestQR = () => {
  try {
    // Store the test invoice
    const storageKey = storeInvoiceOffline(testInvoice)
    const qrData = generateQRCodeData(testInvoice)

    // Create QR code data with storage key
    const qrCodeDataObj = {
      ...qrData,
      storage_key: storageKey
    }

    qrCodeData.value = JSON.stringify(qrCodeDataObj)
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = 'Error generating QR code: ' + error.message
  }
}

const testPDFDownload = async () => {
  try {
    errorMessage.value = ''
    const result = await downloadReceiptPDF(testInvoice)

    if (result.success) {
      alert('PDF رسید با موفقیت دانلود شد!')
    } else {
      errorMessage.value = 'خطا در تولید PDF: ' + result.error
    }
  } catch (error) {
    console.error('Error testing PDF download:', error)
    errorMessage.value = 'خطا در تست دانلود PDF: ' + error.message
  }
}

const testQRScan = () => {
  try {
    scanResult.value = null
    errorMessage.value = ''

    if (!testQRInput.value.trim()) {
      errorMessage.value = 'Please enter QR code data to test'
      return
    }

    const invoice = getInvoiceByQRCode(testQRInput.value)

    if (invoice) {
      scanResult.value = invoice
    } else {
      errorMessage.value = 'Invalid QR code or invoice not found'
    }
  } catch (error) {
    errorMessage.value = 'Error scanning QR code: ' + error.message
  }
}

const testQRScanWithPDF = async () => {
  try {
    scanResult.value = null
    errorMessage.value = ''

    // Use the generated QR code data or test input
    const qrDataToTest = testQRInput.value.trim() || qrCodeData.value

    if (!qrDataToTest) {
      errorMessage.value = 'لطفاً ابتدا QR code تولید کنید یا داده QR را وارد کنید'
      return
    }

    console.log('Testing QR scan with PDF download:', qrDataToTest)

    const invoice = getInvoiceByQRCode(qrDataToTest)

    if (invoice) {
      scanResult.value = invoice
      console.log('Invoice found, starting PDF download...')

      // Automatically download PDF
      const result = await downloadReceiptPDF(invoice)

      if (result.success) {
        alert('✅ موفق! QR اسکن شد و PDF دانلود شد')
      } else {
        errorMessage.value = 'خطا در تولید PDF: ' + result.error
      }
    }

const generateMobileQR = () => {
  try {
    errorMessage.value = ''

    // Generate mobile-compatible QR URL
    const mobileURL = generateMobileQRCodeURL(testInvoice)

    // Set as QR code data
    qrCodeData.value = mobileURL

    // Show success message
    alert(`✅ Mobile QR URL Generated!\n\nURL: ${mobileURL}\n\nThis URL will work on mobile devices and automatically download PDF when scanned!`)

    console.log('Generated mobile QR URL:', mobileURL)

  } catch (error) {
    console.error('Error generating mobile QR:', error)
    errorMessage.value = 'خطا در تولید QR موبایل: ' + error.message
  }
}

const testMobileWorkflow = () => {
  try {
    errorMessage.value = ''

    // Generate mobile QR URL
    const mobileURL = generateMobileQRCodeURL(testInvoice)

    // Set as QR code data
    qrCodeData.value = mobileURL

    // Open mobile page in new tab to simulate mobile scanning
    window.open(mobileURL, '_blank')

    alert(`✅ Mobile workflow test started!\n\nMobile URL: ${mobileURL}\n\nA new tab opened simulating mobile QR scan. The PDF should auto-download!`)

  } catch (error) {
    console.error('Error testing mobile workflow:', error)
    errorMessage.value = 'خطا در تست workflow موبایل: ' + error.message
  }
}

const copyToClipboard = () => {
  navigator.clipboard.writeText(qrCodeData.value).then(() => {
    alert('QR code data copied to clipboard!')
  }).catch(err => {
    console.error('Failed to copy: ', err)
  })
}

const loadInvoice = (invoice) => {
  scanResult.value = invoice
  errorMessage.value = ''
}

const clearStorage = () => {
  if (confirm('Are you sure you want to clear all stored invoices?')) {
    // Clear all invoice data from localStorage
    const keysToRemove = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && (key.startsWith('invoice_') || key === 'invoices_index')) {
        keysToRemove.push(key)
      }
    }

    keysToRemove.forEach(key => {
      localStorage.removeItem(key)
    })

    // Clear current state
    qrCodeData.value = ''
    testQRInput.value = ''
    scanResult.value = null
    errorMessage.value = ''

    alert('All stored invoices cleared!')
  }
}
</script>
